import numpy as np
from structure import Structure
from math import pi as PI
import utilities as util
import json


class Configuration(object):
    """docstring for Config"""
    def __init__(self, struct_1, struct_2):
        # Basic GB settings, required from user input.
        self.struct_1 = struct_1
        self.struct_2 = struct_2
        self.gb_settings = [] # List of GbSetting objects.

        # Coincident point search.
        self.coincident_pts_tolerance = 1.0
        self.coincident_pts_search_step = 25

        # Lattice vector generation.
        self.max_coincident_pts_searched = 100
        self.lattice_vec_agl_range = (0, PI)
        self.atom_counts_range = (5000, 10000)

        # Collision removal.
        self.skip_collision_removal = False
        self.min_atom_dist = {}
        self.boundary_radius = 0.025
        self.random_delete_atom = False

        # Output format.
        self.output_format = ''
        self.output_kwarg = {}
        self.output_dir = ''
        self.output_name_prefix = ''
        self.overwrite_protect = False # TODO: Get a different filename?

    @staticmethod
    def from_gbconf_file(path):
        # First take in the gbconf file and parse JSON.
        with util.open_read_file(path, 'gbconf') as input_file:
            input_json = input_file.read()
            input_file.close()
        parsed_json = json.loads(input_json)
        keys = parsed_json.keys()

        # Parse the two structures.
        if not 'struct_1' in keys:
            raise ValueError('Keyword \'struct_1\' must present'
                             ' in the JSON input file.')
        struct_1 = Structure.from_file(parsed_json['struct_1'])
        if not 'struct_2' in keys:
            raise ValueError('Keyword \'struct_2\' must present'
                             ' in the JSON input file.')
        struct_2 = Structure.from_file(parsed_json['struct_2'])

        config_object = Configuration(struct_1, struct_2)

        # Parse GbSettings.
        if not 'gb_settings' in keys:
            return config_object
        config_object.gb_settings = map(
            lambda x : [np.array(x[0]).astype(float), 
                        np.array(x[1]).astype(float),
                        float(x[2])], 
            parsed_json['gb_settings'])

        # Coincident point search parameters.
        if 'coincident_pts_tolerance' in keys:
            config_object.coincident_pts_tolerance = \
                float(parsed_json['coincident_pts_tolerance'])
        if 'coincident_pts_search_step' in keys:
            config_object.coincident_pts_search_step = \
                int(parsed_json['coincident_pts_search_step'])

        # Lattice vector generation parameters.
        if 'max_coincident_pts_searched' in keys:
            config_object.max_coincident_pts_searched = \
                int(parsed_json['max_coincident_pts_searched'])
        if 'lattice_vec_agl_range' in keys:
            config_object.lattice_vec_agl_range = \
                (float(parsed_json['lattice_vec_agl_range'][0]),
                 float(parsed_json['lattice_vec_agl_range'][1]))
        if 'atom_counts_range' in keys:
            config_object.atom_counts_range = \
                (float(parsed_json['atom_counts_range'][0]),
                 float(parsed_json['atom_counts_range'][1]))

        # Collision removal parameters.
        if 'skip_collision_removal' in keys:
            config_object.skip_collision_removal = \
                parsed_json['skip_collision_removal']
        if 'min_atom_dist' in keys:
            for [atm_1, atm_2, dist] in parsed_json['min_atom_dist']:
                config_object.min_atom_dist[(atm_1, atm_2)] = float(dist)
            if len(config_object.min_atom_dist.keys()) <= 0:
                config_object.skip_collision_removal = True

        if 'boundary_radius' in keys:
            config_object.boundary_radius = \
                float(parsed_json['boundary_radius'])
        if 'random_delete_atom' in keys:
            config_object.random_delete_atom = \
                parsed_json['random_delete_atom']

        # Output format parameters.
        if 'output_format' in keys:
            config_object.output_format = \
                parsed_json['output_format']
        # TODO: Add the kwarg option.
        if 'output_dir' in keys:
            config_object.output_dir = \
                parsed_json['output_dir']
        if 'output_name_prefix' in keys:
            config_object.output_name_prefix = \
                parsed_json['output_name_prefix']
        if 'overwrite_protect' in keys:
            config_object.overwrite_protect = \
                parsed_json['overwrite_protect']

        return config_object


def main():
    Configuration.from_gbconf_file('test.gbconf')

if __name__ == '__main__':
    main()
