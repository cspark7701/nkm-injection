import numpy as np
from nkm_injection.sliced_vector_map import integrated_filament_kicks,sliced_vector_map
from nkm_injection.wire_field import FilamentGeometry,FilamentNKMField,brho_T_m


def test_integrated_kernel_matches_independent_field_integral():
    g=FilamentGeometry();x=np.array([-.0085,-.003,.0002]);y=np.array([.001,.0004,.0001])
    bx,by=FilamentNKMField(g).line_integrals(x,y,s_max_m=2.,n_nodes=2048)
    kx,ky=integrated_filament_kicks(x,y,g)
    assert np.allclose(kx,by/brho_T_m(4e9),atol=1e-10,rtol=1e-7)
    assert np.allclose(ky,-bx/brho_T_m(4e9),atol=1e-10,rtol=1e-7)


def test_vector_kernel_is_curl_free_and_zero_field_limit():
    g=FilamentGeometry();x,y=-.0085,.001;h=1e-7
    dky=(integrated_filament_kicks(x,y+h,g)[0]-integrated_filament_kicks(x,y-h,g)[0])/(2*h)
    dkx=(integrated_filament_kicks(x+h,y,g)[1]-integrated_filament_kicks(x-h,y,g)[1])/(2*h)
    assert np.isclose(dky,dkx,rtol=1e-7)
    b=np.array([x,.005,y,.0002,.002,0.])
    assert np.allclose(sliced_vector_map(b,g,scale=0.),b,atol=1e-14,rtol=0.)
