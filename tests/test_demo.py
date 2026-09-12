import importlib.util
from pathlib import Path
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('generator',ROOT/'scripts/generate_demo_experiments.py')
generator=importlib.util.module_from_spec(spec);spec.loader.exec_module(generator)

def test_reproducible_balanced_and_compatible_demo():
    data=generator.build_experiments(360,42)
    assert data==generator.build_experiments(360,42)
    from collections import Counter
    assert set(Counter((r['procede'],r['materiau']) for r in data).values())=={20}
    assert all(r['limite_endurance']>0 for r in data)
    assert all(r['materiau']=='AlSi7Mg' for r in data if r['revetement']=='Diamant')

def test_browser_projection_and_distances_match_python():
    import json,re
    html=(ROOT/'demo/index.html').read_text()
    data=json.loads(re.search(r'const DATA = (.*);',html).group(1))
    model=json.loads(re.search(r'const MODEL = (.*);',html).group(1))
    features=json.loads(re.search(r'const FEATURES = (.*);',html).group(1))
    x=np.array([[r[f['key']] for f in features] for r in data])
    z=StandardScaler().fit_transform(x);pca=PCA(n_components=6).fit(z)
    projected=((x-model['mean'])/model['scale'])@np.array(model['components']).T
    np.testing.assert_allclose(projected,[r['pc'] for r in data],atol=1e-10)
    np.testing.assert_allclose(projected,pca.transform(z),atol=1e-10)
    np.testing.assert_allclose(model['correlation'],np.corrcoef(x.T),atol=1e-10)
    assert abs(sum(model['explained'])-1)<1e-10
    target=projected[17]
    distances=np.sqrt(np.sum(np.array(model['explained'])*(projected-target)**2,axis=1))
    assert int(np.argmin(distances))==17
