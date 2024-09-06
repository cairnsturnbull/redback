import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)

import redback


sampler = 'nestle'
# lots of different models implemented, including
# afterglow/magnetar varieties/n_dimensional_fireball/shapelets/band function/kilonova/SNe/TDE
model = 'one_component_kilonova_model'

kne = 'at2017gfo'
# gets the magnitude data for AT2017gfo, the KN associated with GW170817
data = redback.get_data.get_kilonova_data_from_open_transient_catalog_data(transient=kne)
# creates a GRBDir with GRB
kilonova = redback.kilonova.Kilonova.from_open_access_catalogue(
    name=kne, data_mode="flux_density", active_bands=np.array(["g", "i"]))
kilonova.plot_data(show=False)
fig, axes = plt.subplots(3, 2, sharex=True, sharey=True, figsize=(12, 8))
kilonova.plot_multiband(figure=fig, axes=axes, filters=["g", "r", "i", "z", "y", "J"], show=False)

# use default priors
priors = redback.priors.get_priors(model=model)
priors['redshift'] = 1e-2

model_kwargs = dict(frequency=kilonova.filtered_frequencies, output_format='flux_density')
result = redback.fit_model(transient=kilonova, model=model, sampler=sampler, model_kwargs=model_kwargs,
                           prior=priors, sample='rslice', nlive=1000, resume=True)
result.plot_corner()
# returns a Kilonova result object
result.plot_lightcurve(show=True)
# Even though we only fit the 'g' band, we can still plot the fit for different bands.
result.plot_multiband_lightcurve(filters=["g", "r", "i", "z", "y", "J"], show=True)
