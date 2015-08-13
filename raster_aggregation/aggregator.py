import json
import traceback

from celery.contrib.methods import task

from raster.models import RasterLayer
from raster.valuecount import aggregator


class Aggregator(object):

    @task()
    def compute_value_count(self, layer_id, simplified=True, compute_area=True):
        """
        Precomputes value counts for all existing rasterlayers.
        """
        from raster_aggregation.models import ValueCountResult

        lyr = RasterLayer.objects.get(id=layer_id)
        if lyr.datatype not in ['ca', 'ma']:
            self.log(
                'ERROR: Rasterlayer {0} is not categorical. '
                'Can only compute value counts on categorical layers'
            )
            return

        # Open parse log
        self.log(
            'Starting Value count for AggregationLayer {agg} on RasterLayer {rst} on {typ} '
            'Geometries'.format(agg=self.id, rst=lyr.id, typ='Simplified' if simplified else 'Original')
        )

        for area in self.aggregationarea_set.all():
            # Remove existing results
            area.valuecountresult_set.all().delete()

            # Get raster layer for agg computation
            rast = RasterLayer.objects.get(id=layer_id)

            self.log('Computing Value Count for area {0} and raster {1}'.format(area.id, rast.id))

            # Get geometry
            if simplified:
                geom = area.geom_simplified
            else:
                geom = area.geom
            try:
                # Prepare data for aggregator
                ids = {'a': rast.id}
                formula = 'a'
                zoom = rast._max_zoom

                # Compute aggregates
                count = aggregator(ids, zoom, geom, formula)

                # Convert keys to string and dump to json
                count = json.dumps({str(key): val for key, val in count.items()})

                # Store result
                ValueCountResult.objects.create(
                    rasterlayer=rast,
                    aggregationarea=area,
                    value=count
                )
            except:
                self.log(
                    'ERROR: Failed to compute value count for '
                    'area {0} and raster {1}'.format(area.id, rast.id)
                )
                self.log(traceback.format_exc())

        self.log(
            'Ended Value count for AggregationLayer {agg} '
            'on RasterLayer {rst}'.format(agg=self.id, rst=lyr.id)
        )
