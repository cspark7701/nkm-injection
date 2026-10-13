"""Round-two BTS diagnostics. Positions/clearances in m, K in m^-2.

Old independent affine predictions remain available for historical audits.
Centred AT Jacobians include the actual shot centroid for new predictions.
"""
from copy import deepcopy
import numpy as np
import at
from .bts_journal import JournalBeam, independent_maps


def unrestricted(lattice):
    """Copy a line without censoring moment probes at its model apertures."""
    result=deepcopy(lattice)
    for elem in result:
        if hasattr(elem,'Limits'):elem.Limits=np.array([-np.inf,np.inf,-np.inf,np.inf])
    return result


def centred_maps(lattice, centroid, step=1e-7):
    """Return AT 5D Jacobians and centroids about a supplied shot [SI]."""
    centroid=np.asarray(centroid,dtype=float)
    if centroid.shape!=(5,) or not np.all(np.isfinite(centroid)):
        raise ValueError('Finite (5,) centroid required')
    if not np.isfinite(step) or step<=0:raise ValueError('Positive probe step required')
    probes=np.zeros((6,11),order='F');probes[:5]=centroid[:,None]
    for j in range(5):probes[j,1+2*j]+=step;probes[j,2+2*j]-=step
    out=at.lattice_track(unrestricted(lattice),probes,nturns=1,refpts=np.arange(len(lattice)+1))[0][:,:,:,0]
    if not np.all(np.isfinite(out)):raise ValueError('Invalid moment probes')
    maps=np.stack([(out[:5,1+2*j]-out[:5,2+2*j])/(2*step) for j in range(5)],axis=-1).transpose(1,0,2)
    return maps,out[:5,0].T


def station_record(lattice, beam=None, centroid=None, beta_factors=(1.,1.), method='affine', step=1e-7):
    """Decompose projected variances at every model aperture, without censoring.

    Betatron and dispersive variances add, rather than their square roots.
    The dispersion component includes momentum correlation and roll coupling.
    """
    beam=beam or JournalBeam();centroid=np.zeros(5) if centroid is None else np.asarray(centroid)
    covariance=beam.covariance(beta_factors)[:5,:5]
    vector=covariance[:,4]/beam.sigma_delta**2
    dispersive=beam.sigma_delta**2*np.outer(vector,vector);betatron=covariance-dispersive
    if method=='affine':
        maps,orbit=independent_maps(lattice);means=orbit+np.einsum('nij,j->ni',maps,centroid)
    elif method=='centred':maps,means=centred_maps(lattice,centroid,step)
    else:raise ValueError('Method must be affine or centred')
    rows=[];s=0.
    for i,elem in enumerate(lattice):
        s+=elem.Length
        if not hasattr(elem,'Limits'):continue
        limits=np.asarray(elem.Limits).reshape(2,2);m=maps[i+1]
        vb=m@betatron@m.T;vd=m@dispersive@m.T
        for axis,j in enumerate([0,2]):
            distance=min(limits[axis,1]-means[i+1,j],means[i+1,j]-limits[axis,0])
            sigma=float(np.sqrt(max(0,vb[j,j]+vd[j,j])))
            rows.append({'index':i,'axis':axis,'s_m':s,'aperture_halfwidth_m':float((limits[axis,1]-limits[axis,0])/2),'centroid_m':float(means[i+1,j]),'betatron_variance_m2':float(vb[j,j]),'dispersive_variance_m2':float(vd[j,j]),'sigma_m':sigma,'clearance_m':float(distance-beam.coverage_sigma*sigma)})
    active=min(rows,key=lambda r:r['clearance_m']);downstream=[r for r in rows if r['s_m']>0]
    return {'stations':rows,'minimum_m':active['clearance_m'],'active':[active['index'],active['axis']], 'downstream_minimum_m':min(r['clearance_m'] for r in downstream)}


def set_regime(lattice, restrictions):
    """Set symmetric hypothetical halfwidths [m] on a copied line."""
    result=deepcopy(lattice)
    for index,widths in restrictions.items():
        x,y=widths
        if min(x,y)<=0:raise ValueError('Positive aperture halfwidths required')
        result[int(index)].Limits=np.array([-x,x,-y,y])
    return result


def quadrature_moments(lattice, beam, centroid, beta_factors=(1.,1.), order=5):
    """Gaussian product quadrature of uncensored AT moments, in m and m^2.

    Deterministic quadrature avoids random RMS uncertainty. Order convergence
    must be checked; this is not a certification of Gaussian loss tails.
    """
    from numpy.polynomial.hermite import hermgauss
    nodes,weights=hermgauss(order)
    grid=np.array(np.meshgrid(*([nodes]*5),indexing='ij')).reshape(5,-1)
    wgrid=np.array(np.meshgrid(*([weights/np.sqrt(np.pi)]*5),indexing='ij')).reshape(5,-1)
    w=np.prod(wgrid,axis=0)
    cov=beam.covariance(beta_factors)[:5,:5];e,v=np.linalg.eigh(cov)
    transform=v@np.diag(np.sqrt(np.maximum(e,0)))
    particles=np.zeros((6,order**5),order='F');particles[:5]=np.asarray(centroid)[:,None]+transform@(np.sqrt(2)*grid)
    out=at.lattice_track(unrestricted(lattice),particles,nturns=1,refpts=np.arange(len(lattice)+1))[0][:5,:,:,0]
    if not np.all(np.isfinite(out)):raise ValueError('Invalid quadrature coordinates')
    mean=np.einsum('j,ijk->ki',w,out)
    deviations=out-mean.T[:,None,:]
    variance=np.einsum('j,ijk->ki',w,deviations**2)
    return mean,np.sqrt(np.maximum(variance,0))
