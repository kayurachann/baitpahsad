"""StegaGuard research pipeline. See README.md for protocol and limitations."""
from pathlib import Path
import argparse, csv, hashlib, json, random, struct, sys, time
import numpy as np
from PIL import Image
 
ALGORITHMS = ('wow', 'suniward', 'hill')
 
def digest(data):
    return hashlib.sha256(data).hexdigest()
 
def write_json(path, data):
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
 
def lsb_encode(image, message):
    """Teaching example: 32-bit length prefix + bytes, sequential LSB replacement."""
    x = np.asarray(image, dtype=np.uint8).copy()
    packet = struct.pack('>I', len(message)) + message
    bits = np.unpackbits(np.frombuffer(packet, dtype=np.uint8))
    if len(bits) > x.size:
        raise ValueError('Message exceeds capacity')
    flat = x.reshape(-1)
    flat[:len(bits)] = (flat[:len(bits)] & 254) | bits
    return x
 
def lsb_decode(image):
    flat = np.asarray(image, dtype=np.uint8).reshape(-1)
    if flat.size < 32:
        raise ValueError('Image too small')
    n = int.from_bytes(np.packbits(flat[:32] & 1).tobytes(), 'big')
    if 32 + n * 8 > flat.size:
        raise ValueError('Invalid length prefix')
    return np.packbits(flat[32:32+n*8] & 1).tobytes()
 
def prepare(args):
    """Split unique covers first; then simulate all variants within each split."""
    import conseal
    root = Path(args.out)
    if root.exists():
        raise ValueError('Output already exists; choose a new directory')
    paths = sorted(p for p in Path(args.covers).rglob('*') if p.suffix.lower() in ('.pgm','.png','.bmp','.tif','.tiff'))
    if args.limit:
        random.Random(args.seed).shuffle(paths)
        paths = paths[:args.limit]
    covers, seen = [], set()
    for path in paths:
        with Image.open(path) as im:
            if im.mode != 'L':
                raise ValueError(f'{path}: expected 8-bit grayscale; do not silently convert colors')
            if args.size:
                im = im.resize((args.size, args.size), Image.Resampling.BICUBIC)
            x = np.asarray(im).copy()
        sha = digest(str(x.shape).encode() + x.tobytes())
        if sha not in seen:
            covers.append((path, x, sha)); seen.add(sha)
    if len(covers) < 10:
        raise ValueError('At least 10 unique covers required')
    if len({x.shape for _, x, _ in covers}) != 1:
        raise ValueError('All covers must have equal dimensions; use --size before embedding')
    rng = np.random.default_rng(args.seed)
    order = rng.permutation(len(covers))
    ntrain, nval = int(.6*len(covers)), int(.2*len(covers))
    splits = {int(j): ('train' if i<ntrain else 'val' if i<ntrain+nval else 'test') for i,j in enumerate(order)}
    root.mkdir(parents=True)
    rows = []
    for index, (source,x,sha) in enumerate(covers):
        cover_id = sha[:20]
        base = root / 'images' / cover_id
        base.mkdir(parents=True)
        def save(y, algorithm, payload, embed_seed):
            filename = 'cover.png' if algorithm=='cover' else f'{algorithm}_{payload:g}.png'
            target = base / filename
            Image.fromarray(y).save(target)
            rows.append(dict(cover_id=cover_id,split=splits[index],path=target.relative_to(root).as_posix(),
                label=int(algorithm!='cover'),algorithm=algorithm,payload=payload,embedding_seed=embed_seed,
                sha256=digest(target.read_bytes()),source_sha256=sha,source_name=source.name))
        save(x,'cover',0,0)
        for algorithm in args.algorithms:
            for payload in args.payloads:
                if not 0 < payload <= 1:
                    raise ValueError('Payload must be in (0,1] bpp')
                seed = int(digest(f'{args.seed}:{sha}:{algorithm}:{payload}'.encode())[:8],16)
                y = getattr(conseal,algorithm).simulate_single_channel(x0=x,alpha=payload,seed=seed)
                y = np.asarray(y)
                if y.shape != x.shape or not np.isfinite(y).all() or y.min()<0 or y.max()>255 or not np.equal(y,np.rint(y)).all():
                    raise ValueError('Invalid simulator output')
                y = y.astype(np.uint8)
                if np.abs(y.astype(int)-x.astype(int)).max()>1:
                    raise ValueError('Unexpected modification magnitude')
                save(y,algorithm,payload,seed)
    with (root/'manifest.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    write_json(root/'preparation.json',dict(seed=args.seed,size_before_embedding=args.size,
        unique_covers=len(covers),split='60/20/20',algorithms=args.algorithms,payloads=args.payloads,
        simulator='conseal; ideal embedding simulation, no recoverable message',
        manifest_sha256=digest((root/'manifest.csv').read_bytes())))
    audit(root)
 
def read_rows(root):
    with (Path(root)/'manifest.csv').open(encoding='utf-8') as f:
        return list(csv.DictReader(f))
 
def audit(root):
    rows=read_rows(root); groups={}; hash_splits={}; pixel_splits={}; paths=set()
    for row in rows:
        if row['split'] not in ('train','val','test') or row['label'] not in ('0','1'):
            raise ValueError('Invalid split or label')
        if row['path'] in paths: raise ValueError('Duplicate manifest path')
        paths.add(row['path'])
        target=(Path(root)/row['path']).resolve()
        if not target.is_relative_to(Path(root).resolve()): raise ValueError('Path escapes dataset')
        if digest(target.read_bytes()) != row['sha256']: raise ValueError('File hash mismatch')
        with Image.open(target) as im:
            if im.mode!='L': raise ValueError('Expected grayscale')
            px=digest(str(im.size).encode()+np.asarray(im).tobytes())
        groups.setdefault(row['cover_id'],[]).append(row)
        hash_splits.setdefault(row['source_sha256'],set()).add(row['split'])
        pixel_splits.setdefault(px,set()).add(row['split'])
    for group in groups.values():
        if len({r['split'] for r in group})!=1: raise ValueError('Cover leakage')
        if sum(r['label']=='0' for r in group)!=1: raise ValueError('Expected one cover per group')
    if any(len(s)>1 for s in list(hash_splits.values())+list(pixel_splits.values())):
        raise ValueError('Duplicate source or pixels across splits')
    result=dict(status='PASS',unique_covers=len(groups),images=len(rows),
        covers_by_split={s:sum(g[0]['split']==s for g in groups.values()) for s in ('train','val','test')})
    write_json(Path(root)/'audit.json',result)
    return result
 
def pairs(root, split, algorithms, payloads):
    rows=read_rows(root)
    covers={r['cover_id']:r for r in rows if r['label']=='0' and r['split']==split}
    result=[(covers[r['cover_id']],r) for r in rows if r['split']==split and r['label']=='1'
        and r['algorithm'] in algorithms and any(abs(float(r['payload'])-p)<1e-8 for p in payloads)]
    if not result: raise ValueError('No examples for requested condition')
    return result
 
def pixels(root,row):
    with Image.open(Path(root)/row['path']) as im:
        return np.asarray(im,dtype=np.float32).copy()
 
def residual_features(x):
    """Small transparent baseline, NOT the full Spatial Rich Model (SRM)."""
    blocks=[]
    for delta in (np.diff(x,axis=0),np.diff(x,axis=1),np.diff(x,n=2,axis=0),np.diff(x,n=2,axis=1)):
        hist=np.histogram(np.clip(delta,-8,8),bins=np.arange(-8.5,9.5,1))[0].astype(float)
        blocks.extend(hist/max(1,hist.sum()))
        blocks.extend([np.mean(np.abs(delta)),np.std(delta)])
    return np.asarray(blocks)
 
def scores_metrics(labels,scores,threshold):
    from sklearn.metrics import roc_auc_score,accuracy_score,precision_score,recall_score,f1_score,confusion_matrix
    y=np.asarray(labels);s=np.asarray(scores);pred=s>=threshold
    tn,fp,fn,tp=confusion_matrix(y,pred,labels=[0,1]).ravel()
    return dict(n=len(y),auc=float(roc_auc_score(y,s)),accuracy=float(accuracy_score(y,pred)),
        precision=float(precision_score(y,pred,zero_division=0)),recall=float(recall_score(y,pred,zero_division=0)),
        f1=float(f1_score(y,pred,zero_division=0)),fpr=float(fp/(fp+tn)),fnr=float(fn/(fn+tp)),
        balanced_error=float(.5*(fp/(fp+tn)+fn/(fn+tp))),tn=int(tn),fp=int(fp),fn=int(fn),tp=int(tp))
 
def thresholds(labels,scores,target=.01):
    """Select on validation only. Scores may be logits or decision scores."""
    from sklearn.metrics import roc_curve
    y=np.asarray(labels);s=np.asarray(scores)
    fpr,tpr,t=roc_curve(y,s,drop_intermediate=False)
    finite=np.isfinite(t); t=t[finite]; err=.5*(fpr[finite]+1-tpr[finite])
    best=float(t[np.argmin(err)])
    cover=np.sort(s[y==0])[::-1]; k=int(np.floor(target*len(cover)))
    low=float(np.nextafter(cover[k],np.inf))
    return dict(balanced=best,low_fpr=low,target_validation_fpr=target)
 
def train(args):
    import torch
    from torch.utils.data import DataLoader,TensorDataset
    from models import make_model
    torch.set_num_threads(args.threads)
    random.seed(args.seed);np.random.seed(args.seed);torch.manual_seed(args.seed)
    if torch.cuda.is_available(): torch.cuda.manual_seed_all(args.seed)
    torch.backends.cudnn.benchmark=False;torch.backends.cudnn.deterministic=True
    audit(args.data)
    output=Path(args.out);output.mkdir(parents=True,exist_ok=False)
    tr=pairs(args.data,'train',args.algorithms,args.payloads)
    va=pairs(args.data,'val',args.algorithms,args.payloads)
    config=vars(args).copy();config.pop('func',None)
    config['data']=str(Path(args.data).resolve())
    config['manifest_sha256']=digest((Path(args.data)/'manifest.csv').read_bytes())
    write_json(output/'config.json',config)
    started=time.time()
    if args.model=='residual_lr':
        import joblib
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler
        from sklearn.linear_model import LogisticRegression
        # One variant per source controls sample count for mixed/single comparison.
        groups={}
        for c,s in tr:groups.setdefault(c['cover_id'],[]).append((c,s))
        rr=random.Random(args.seed);selected=[rr.choice(g) for g in groups.values()]
        records=[r for pair in selected for r in pair]
        model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=2000,random_state=args.seed))
        model.fit(np.stack([residual_features(pixels(args.data,r)) for r in records]),[int(r['label']) for r in records])
        joblib.dump(model,output/'model.joblib')
        y,s=score_pairs(args.data,va,model,'residual_lr','cpu')
        history=[dict(epoch=1,validation_auc=scores_metrics(y,s,0)['auc'])]
    else:
        device='cuda' if args.device=='auto' and torch.cuda.is_available() else ('cpu' if args.device=='auto' else args.device)
        model=make_model(args.model).to(device)
        optimizer=torch.optim.Adamax(model.parameters(),lr=args.lr,weight_decay=1e-4)
        criterion=torch.nn.CrossEntropyLoss()
        groups={}
        for c,s in tr:groups.setdefault(c['cover_id'],[]).append((c,s))
        history=[];best=float('inf')
        for epoch in range(args.epochs):
            model.train(); rr=random.Random(args.seed+epoch)
            selected=[rr.choice(g) for g in groups.values()];rr.shuffle(selected)
            total=0.;count=0
            # Pair mini-batches remain 1:1 cover/stego; same lossless transform per pair.
            for start in range(0,len(selected),args.batch_pairs):
                batch=selected[start:start+args.batch_pairs]; xs=[];ys=[]
                for c,s in batch:
                    turns=rr.randrange(4);flip=rr.choice([False,True])
                    for r in (c,s):
                        x=pixels(args.data,r);x=np.rot90(x,turns)
                        if flip:x=np.fliplr(x)
                        xs.append(x.copy()[None]/255.);ys.append(int(r['label']))
                x=torch.from_numpy(np.stack(xs)).to(device);y=torch.tensor(ys,device=device)
                optimizer.zero_grad();loss=criterion(model(x),y);loss.backward();optimizer.step()
                total+=loss.item()*len(ys);count+=len(ys)
            y,s=score_pairs(args.data,va,model,args.model,device)
            # Stable logistic cross entropy from the logit difference.
            val_loss=float(np.mean(np.logaddexp(0,s)-np.asarray(y)*s))
            history.append(dict(epoch=epoch+1,train_loss=total/count,validation_loss=val_loss))
            if val_loss<best:
                best=val_loss;torch.save(model.state_dict(),output/'model.pt')
            print(json.dumps(history[-1]),flush=True)
        model.load_state_dict(torch.load(output/'model.pt',map_location=device,weights_only=True))
        y,s=score_pairs(args.data,va,model,args.model,device)
    # Deduplicate validation covers for FPR calibration, retain stego variants.
    flat=[r for pair in va for r in pair];seen=set();keep=[]
    for i,r in enumerate(flat):
        if r['path'] not in seen:keep.append(i);seen.add(r['path'])
    th=thresholds(np.asarray(y)[keep],np.asarray(s)[keep])
    write_json(output/'thresholds.json',th);write_json(output/'history.json',history)
    write_json(output/'runtime.json',dict(seconds=time.time()-started,torch=torch.__version__,cuda_available=torch.cuda.is_available()))
 
def score_pairs(root,pair_list,model,kind,device):
    records=[r for pair in pair_list for r in pair]
    y=[int(r['label']) for r in records]
    if kind=='residual_lr':
        return y,model.decision_function(np.stack([residual_features(pixels(root,r)) for r in records]))
    import torch
    model.eval();scores=[]
    with torch.no_grad():
        for start in range(0,len(records),16):
            x=np.stack([pixels(root,r)[None]/255. for r in records[start:start+16]])
            z=model(torch.from_numpy(x).to(device)).cpu().numpy()
            scores.extend(z[:,1]-z[:,0])
    return y,np.asarray(scores)
 
def evaluate(args):
    import torch
    from models import make_model
    torch.set_num_threads(args.threads)
    audit(args.data)
    run=Path(args.run);config=json.loads((run/'config.json').read_text())
    if digest((Path(args.data)/'manifest.csv').read_bytes())!=config['manifest_sha256']:
        raise ValueError('Manifest differs from training; external validation needs a separate protocol')
    th=json.loads((run/'thresholds.json').read_text());kind=config['model']
    if kind=='residual_lr':
        import joblib
        model=joblib.load(run/'model.joblib')
    else:
        model=make_model(kind);model.load_state_dict(torch.load(run/'model.pt',map_location='cpu',weights_only=True))
    out=Path(args.out);out.mkdir(parents=True,exist_ok=False);summaries=[];predictions=[]
    for algorithm in args.algorithms:
        for payload in args.payloads:
            pp=pairs(args.data,'test',[algorithm],[payload]);y,s=score_pairs(args.data,pp,model,kind,'cpu')
            metrics=scores_metrics(y,s,th['balanced']);low=scores_metrics(y,s,th['low_fpr'])
            rng=np.random.default_rng(2026);aucs=[]
            for _ in range(args.bootstrap):
                ids=rng.integers(0,len(pp),len(pp));ix=np.array([[2*i,2*i+1] for i in ids]).ravel()
                aucs.append(scores_metrics(np.asarray(y)[ix],s[ix],th['balanced'])['auc'])
            row=dict(model=kind,algorithm=algorithm,payload=payload,unseen_algorithm=algorithm not in config['algorithms'],
                threshold=th['balanced'],**metrics,recall_at_validation_low_fpr=low['recall'],actual_test_fpr=low['fpr'],
                auc_ci_low=float(np.quantile(aucs,.025)) if aucs else None,
                auc_ci_high=float(np.quantile(aucs,.975)) if aucs else None)
            summaries.append(row)
            for r,score in zip([r for pair in pp for r in pair],s):
                predictions.append(dict(cover_id=r['cover_id'],path=r['path'],label=int(r['label']),
                    test_algorithm=algorithm,payload=payload,score=float(score)))
    for filename,rows in [('metrics.csv',summaries),('predictions.csv',predictions)]:
        with (out/filename).open('w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    write_json(out/'evaluation.json',dict(run=str(run.resolve()),bootstrap=args.bootstrap,unit='cover-stego pair',
        threshold_source='validation only',data_manifest=config['manifest_sha256']))
 
def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    a=sub.add_parser('prepare');a.add_argument('--covers',required=True);a.add_argument('--out',required=True)
    a.add_argument('--size',type=int,default=256);a.add_argument('--limit',type=int,default=0)
    a.add_argument('--seed',type=int,default=2026);a.set_defaults(func=prepare)
    b=sub.add_parser('audit');b.add_argument('--data',required=True);b.set_defaults(func=lambda x:print(audit(x.data)))
    t=sub.add_parser('train');t.add_argument('--data',required=True);t.add_argument('--out',required=True)
    t.add_argument('--model',choices=['cnn','resnet18','srnet','residual_lr'],required=True)
    t.add_argument('--epochs',type=int,default=100);t.add_argument('--batch-pairs',type=int,default=4)
    t.add_argument('--lr',type=float,default=.001);t.add_argument('--seed',type=int,default=42)
    t.add_argument('--device',default='auto');t.add_argument('--threads',type=int,default=2);t.set_defaults(func=train)
    e=sub.add_parser('evaluate');e.add_argument('--data',required=True);e.add_argument('--run',required=True)
    e.add_argument('--out',required=True);e.add_argument('--bootstrap',type=int,default=1000)
    e.add_argument('--threads',type=int,default=2);e.set_defaults(func=evaluate)
    for parser in (a,t,e):
        parser.add_argument('--algorithms',nargs='+',choices=ALGORITHMS,default=list(ALGORITHMS))
        parser.add_argument('--payloads',nargs='+',type=float,default=[.1,.2,.4])
    args=p.parse_args()
    if getattr(args,'epochs',1)<1 or getattr(args,'batch_pairs',1)<1: p.error('Positive training settings required')
    args.func(args)
 
if __name__=='__main__':main()
