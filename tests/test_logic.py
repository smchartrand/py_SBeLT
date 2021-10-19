import unittest
import random
import numpy as np
from mock import MagicMock


from model import logic

ATTR_COUNT = 7 # Number of attributes associated with a Particle
# For reference:
        # [0] = x-coord
        # [1] = diameter,
        # [2] = y-coord (elevation),
        # [3] = uid,
        # [4] = active (boolean)
        # [5] = age counter
        # [6] = loop age counter
  
class TestGetEventParticlesWithOneSubregion(unittest.TestCase):

    def setUp(self):
        self.test_length = 10
        self.num_particles = 3

        mock_subregion = MagicMock()
        mock_subregion.leftBoundary.return_value = 0
        mock_subregion.rightBoundary.return_value = self.test_length
        mock_subregion.getName.return_value = 'Mock_Subregion'
        self.mock_sub_list = [mock_subregion]

        self.entrainment_events = 3
        self.level_limit = random.randint(0, random.randint(2, 10))


    def test_all_active_returns_valid_list(self):
        
        model_particles = np.zeros((self.num_particles, ATTR_COUNT))
        model_particles[:,3] = np.arange(self.num_particles) # unique ids
        model_particles[:,4] = np.ones(self.num_particles) # all active
        model_particles[:,0] = np.random.randint(
                                                self.test_length, 
                                                size=self.num_particles ) # random placement

        list = logic.get_event_particles(
                                        self.entrainment_events, 
                                        self.mock_sub_list, 
                                        model_particles, 
                                        self.level_limit )
        self.assertCountEqual(list, model_particles[:,3])

        # Height dependancy should not effect list results here
        hp_list = list = logic.get_event_particles(
                                        self.entrainment_events, 
                                        self.mock_sub_list, 
                                        model_particles, 
                                        self.level_limit,
                                        height_dependant=True )
        self.assertCountEqual(hp_list, model_particles[:,3])
        self.assertCountEqual(hp_list, list)
    
    # TODO: Mock logging object and assert warning is logged
    def test_not_all_active_returns_list_of_2(self):

        mp_one_inactive = np.zeros((self.num_particles, ATTR_COUNT))
        mp_one_inactive[:,3] = np.arange(self.num_particles) 
        mp_one_inactive[0][4] = 1
        mp_one_inactive[1][4] = 1
        mp_one_inactive[:,0] = np.random.randint(self.test_length, size=self.num_particles)

        list = logic.get_event_particles(
                                        self.entrainment_events, 
                                        self.mock_sub_list, 
                                        mp_one_inactive, 
                                        self.level_limit )
        self.assertEqual(len(list), self.num_particles - 1)
        active_list = mp_one_inactive[mp_one_inactive[:,4] != 0]
        self.assertCountEqual(list, active_list[:,3])

    # TODO: Mock logging object and assert warning is logged
    def test_none_active_returns_empty_list(self):
        
        np_none_active = np.zeros((self.num_particles, ATTR_COUNT))
        np_none_active[:,3] = np.arange(self.num_particles) 
        np_none_active[:,0] = np.random.randint(self.test_length, size=self.num_particles)

        empty_list = logic.get_event_particles(
                                        self.entrainment_events, 
                                        self.mock_sub_list, 
                                        np_none_active, 
                                        self.level_limit )
        self.assertEqual(len(empty_list), 0)
    

    def test_all_ghost_particles_returns_ghost_particles(self):
        
        np_all_ghost = np.zeros((self.num_particles, ATTR_COUNT))
        np_all_ghost[:,3] = np.arange(self.num_particles) 
        np_all_ghost[:,0] = -1

        ghost_list = logic.get_event_particles(
                                        self.entrainment_events, 
                                        self.mock_sub_list, 
                                        np_all_ghost, 
                                        self.level_limit )
        self.assertCountEqual(ghost_list, np_all_ghost[:,3])

    def test_some_ghost_particles_returns_ghost_and_regular(self):
        
        np_all_ghost = np.zeros((self.num_particles, ATTR_COUNT))
        np_all_ghost[:,3] = np.arange(self.num_particles) 
        np_all_ghost[:,0] = -1

        ghost_list = logic.get_event_particles(
                                        self.entrainment_events, 
                                        self.mock_sub_list, 
                                        np_all_ghost, 
                                        self.level_limit )
        self.assertCountEqual(ghost_list, np_all_ghost[:,3])     

    # Do we need a tear down method?

class TestGetEventParticlesWithNSubregions(unittest.TestCase):
    
    def setUp(self):
        self.test_length = 20
        self.num_particles = 6

        mock_subregion_0 = MagicMock()
        mock_subregion_0.leftBoundary.return_value = 0
        mock_subregion_0.rightBoundary.return_value = self.test_length / 2
        mock_subregion_0.getName.return_value = 'Mock_Subregion_0'

        mock_subregion_1 = MagicMock()
        mock_subregion_1.leftBoundary.return_value = self.test_length / 2
        mock_subregion_1.rightBoundary.return_value = self.test_length
        mock_subregion_1.getName.return_value = 'Mock_Subregion_1'

        self.mock_sub_list_2 = [mock_subregion_0, mock_subregion_1]

        self.entrainment_events = 3
        self.level_limit = random.randint(0, random.randint(2, 10))


    def test_all_active_returns_3_per_subregion(self):
        
        model_particles = np.zeros((self.num_particles, ATTR_COUNT))
        model_particles[:,3] = np.arange(self.num_particles) # unique ids
        model_particles[:,4] = np.ones(self.num_particles) # all active
        # Randomly place first three particles in Subregion 1 
        model_particles[0:3, 0] = np.random.randint(
                                                10, 
                                                size=3 )
        # Randomly place last three particles in Subregion 2
        model_particles[3:6, 0] = np.random.randint(
                                                10,
                                                self.test_length, 
                                                size=3 )

        list = logic.get_event_particles(
                                        self.entrainment_events, 
                                        self.mock_sub_list_2, 
                                        model_particles, 
                                        self.level_limit )
        self.assertCountEqual(list, model_particles[:,3])
        self.assertEqual(len(list), self.entrainment_events * 2)

        # Height dependancy should not effect list results here
        hp_list = list = logic.get_event_particles(
                                        self.entrainment_events, 
                                        self.mock_sub_list_2, 
                                        model_particles, 
                                        self.level_limit,
                                        height_dependant=True )
        self.assertCountEqual(hp_list, model_particles[:,3])
        self.assertCountEqual(hp_list, list)


    def test_active_in_1_subregion_returns_only_active(self):
        
        mp_half_active = np.zeros((self.num_particles, ATTR_COUNT))
        mp_half_active[:,3] = np.arange(self.num_particles) 
        mp_half_active[0:3, 4] = np.ones(int((self.num_particles/2))) # First half active

        mp_half_active[0:3, 0] = np.random.randint(10,size=3 )
        mp_half_active[3:6, 0] = np.random.randint(10, self.test_length, size=3 ) 

        list = logic.get_event_particles(
                                        self.entrainment_events, 
                                        self.mock_sub_list_2, 
                                        mp_half_active, 
                                        self.level_limit )

        active_particles = mp_half_active[mp_half_active[:,4] != 0] 

        self.assertCountEqual(list, active_particles[:,3])
        self.assertEqual(len(list), 3)
    
    def test_particle_on_boundary_is_not_returned_twice(self):
        
        one_particle_on_boundary = np.zeros((1, ATTR_COUNT))
        one_particle_on_boundary[0][4] = 1
        one_particle_on_boundary[0][0] = 10
        # Use custom entrainment_event count for simplicity
        entrainment_events = 1

        list = logic.get_event_particles(
                                        entrainment_events, 
                                        self.mock_sub_list_2, 
                                        one_particle_on_boundary, 
                                        self.level_limit )
        self.assertEqual(len(list), 1)

# Test Define Subregions
class TestDefineSubregions(unittest.TestCase):

    def setUp(self):
        self.bed_length = 10
        self.iterations = 10
    
    def test_bad_subregion_count_returns_value_error(self):
        subregion_count = 3
        with self.assertRaises(ValueError):
            subregion_list = logic.define_subregions(self.bed_length, 
                                                    subregion_count, 
                                                    self.iterations)

        subregion_zero = 0
        with self.assertRaises(ValueError):
            subregion_list = logic.define_subregions(self.bed_length, 
                                                    subregion_zero, 
                                                    self.iterations)

    def test_good_parameters_return_good_subregion_list(self):
        subregion_count_even = 2
        left_boundary = 0
        middle_boundary = self.bed_length / 2
        right_boundary = self.bed_length

        subregion_list = logic.define_subregions(self.bed_length, 
                                                subregion_count_even, 
                                                self.iterations)
        # Check number of subregions
        self.assertEqual(len(subregion_list), 2) 
        # Check boundary definitions
        self.assertEqual(subregion_list[0].leftBoundary(), left_boundary)
        self.assertEqual(subregion_list[0].rightBoundary(), middle_boundary)
        self.assertEqual(subregion_list[1].leftBoundary(), middle_boundary)
        self.assertEqual(subregion_list[1].rightBoundary(), right_boundary)

        subregion_count_odd = 5
        sub_length = self.bed_length / subregion_count_odd

        left_boundary = 0
        middle_boundary_1 = left_boundary + sub_length*1
        middle_boundary_2 = left_boundary + sub_length*2
        middle_boundary_3 = left_boundary + sub_length*3
        middle_boundary_4 = left_boundary + sub_length*4
        right_boundary = self.bed_length

        subregion_list_odd = logic.define_subregions(self.bed_length, 
                                                subregion_count_odd, 
                                                self.iterations)
        # Check number of subregions
        self.assertEqual(len(subregion_list_odd), 5) 
        # Check boundary definitions
        self.assertEqual(subregion_list_odd[0].leftBoundary(), left_boundary)
        self.assertEqual(subregion_list_odd[0].rightBoundary(), middle_boundary_1)
        self.assertEqual(subregion_list_odd[1].leftBoundary(), middle_boundary_1)
        self.assertEqual(subregion_list_odd[1].rightBoundary(), middle_boundary_2)
        self.assertEqual(subregion_list_odd[2].leftBoundary(), middle_boundary_2)
        self.assertEqual(subregion_list_odd[2].rightBoundary(), middle_boundary_3)
        self.assertEqual(subregion_list_odd[3].leftBoundary(), middle_boundary_3)
        self.assertEqual(subregion_list_odd[3].rightBoundary(), middle_boundary_4)
        self.assertEqual(subregion_list_odd[4].leftBoundary(), middle_boundary_4)
        self.assertEqual(subregion_list_odd[4].rightBoundary(), right_boundary)
    
    def test_all_subregion_flux_are_init_0(self):
        subregion_count_even = 2
        empty_list = np.zeros(self.iterations, dtype=np.int64)
        subregion_list = logic.define_subregions(self.bed_length, 
                                                subregion_count_even, 
                                                self.iterations)
        
        for subregion in subregion_list:
            self.assertEqual(len(subregion.getFluxList()), self.iterations)
            self.assertCountEqual(subregion.getFluxList(), empty_list)


# # Test Add Bed Particle
# class TestAddBedParticle():


# # Test Build Streambed
# class TestBuildStreambed():



if __name__ == '__main__':
    unittest.main()