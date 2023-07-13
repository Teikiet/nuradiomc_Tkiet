import json


class Detector:
    # idk why these "optional" keywords are necessary. I get
    # errors if I don't have these...
    CHANNEL_TEMPLATE = {
        "commission_time": "{TinyDate}:2000-01-01T00:00:00",
        "decommission_time": "{TinyDate}:2040-01-01T00:00:00",
        "adc_sampling_frequency": 1.0,
        "adc_n_samples": 512,
        "cab_time_delay": 19.8,
    }
    STATION_DEFAULT_ID = 101

    def __init__(self):
        self.is_default = False
        self.channels = {}
        self.stations = {}

    @property
    def detector(self):
        return {"channels": self.channels, "stations": self.stations}

    @property
    def num_channels(self):
        return len(self.channels)

    def station_default(self):
        self.is_default = True
        self.stations = {
            self.STATION_DEFAULT_ID: {
                "station_id": self.STATION_DEFAULT_ID,
                "pos_altitude": 0,
                "pos_easting": 0,
                "pos_northing": 0,
                "pos_site": "southpole",
                "commission_time": "{TinyDate}:2000-01-01T00:00:00",
                "decommission_time": "{TinyDate}:2040-01-01T00:00:00",
            }
        }

    def create_channel(self, det, x, y, z, orientation, rotation, station_id=0):
        if self.is_default:
            station_id = 101
        info = {
            "channel_id": self.num_channels,
            "station_id": station_id,
            "ant_type": det,
            "ant_position_x": x,
            "ant_position_y": y,
            "ant_position_z": z,
            "ant_orientation_theta": orientation["theta"],
            "ant_orientation_phi": orientation["phi"],
            "ant_rotation_theta": rotation["theta"],
            "ant_rotation_phi": rotation["phi"],
        }

        info.update(self.CHANNEL_TEMPLATE)
        self.channels.update({info["channel_id"]: info})

    def create_json(self, output_name, print_confirm=True):
        with open(f"{output_name}.json", "w") as f:
            json.dump(self.detector, f, indent=4)
        if print_confirm:
            print(f"Created JSON '{output_name}.json'.")
