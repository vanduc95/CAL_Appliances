import hashlib
import random
from math import floor

FINGER_TABLE_SIZE = 8
RING_SIZE = 2 ** FINGER_TABLE_SIZE


class Ring(object):
    def __init__(self, username, clouds):
        self.id = int(hashlib.sha256(username).hexdigest(), 16) % RING_SIZE
        self.size = RING_SIZE
        self.nodes = []
        # clouds = [cloud1, cloud2, cloud3...]
        # # cloud1 = Cloud(type, config, address)
        # # cloud1 is an instance of class Cloud
        self.clouds = clouds
        self._gen_clouds_duplicate_list()

    def generate_ring(self):
        pass

    def _calculate_sum_quota(self):
        """Calculate sum quota"""
        _sum = 0
        for cloud in self.clouds:
            _sum += cloud.quota
        return _sum

    def _set_weight_cloud(self):
        """Set cloud's weight:
        cloud.weight = cloud.quota / sum_quota"""
        for cloud in self.clouds:
            cloud.set_weight(self._calculate_sum_quota())

    def _gen_clouds_duplicate_list(self):
        """Create n duplicates per cloud."""
        self.duplicates = []
        # Number of duplicates (all clouds)
        total_duplicates = RING_SIZE * 3
        # Number duplicates per cloud (int)
        num_dupl_per_cloud = []
        for cloud in self.clouds:
            num_dupl_per_cloud.append(floor(cloud.weight * total_duplicates))
        # Re-check
        if sum(num_dupl_per_cloud) != total_duplicates:
            rand_elm = random.randrange(0, len(num_dupl_per_cloud))
            num_dupl_per_cloud[rand_elm] += (total_duplicates - sum(num_dupl_per_cloud))
        # Create multi references of one cloud object.
        for map in zip(self.clouds, num_dupl_per_cloud):
            for i in range(map[1]):
                _fork = map[0]
                self.duplicates.append(_fork)
        # Shuffle duplicates
        random.shuffle(self.duplicates)