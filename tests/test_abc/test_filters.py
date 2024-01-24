# ruff: noqa
import unittest

import ongaku


class FilterTest(unittest.TestCase):
    def test_volume(self):
        test_filter = ongaku.Filter()

        test_filter.volume(30.2)

        filter_build = test_filter._build()

        assert filter_build["volume"] == 30.2

    def test_equalizer(self):
        test_filter = ongaku.Filter()

        test_filter.set_equalizer(ongaku.BandType.HZ40, 0.54)

        with self.assertRaises(ValueError):
            test_filter.set_equalizer(ongaku.BandType.HZ100, -0.26)

        with self.assertRaises(ValueError):
            test_filter.set_equalizer(ongaku.BandType.HZ100, 1.1)

        filter_build = test_filter._build()

        assert filter_build["equalizer"][0]["band"] == ongaku.BandType.HZ40.value  # type: ignore
        assert filter_build["equalizer"][0]["gain"] == 0.54  # type: ignore

    def test_karaoke(self):
        with self.assertRaises(ValueError):
            test_filter_error = ongaku.Filter()

            test_filter_error.set_karaoke(level=1.1)
            test_filter_error.set_karaoke(mono_level=1.1)

        with self.assertRaises(ValueError):
            test_filter_error = ongaku.Filter()

            test_filter_error.set_karaoke(level=-0.1)
            test_filter_error.set_karaoke(mono_level=-0.1)

        test_filter = ongaku.Filter()

        test_filter.set_karaoke(
            level=0.89,
            mono_level=0.64,
            filter_band=12.1,
            filter_width=3.2,
        )

        filter_build = test_filter._build()

        assert filter_build["karaoke"]["level"] == 0.89  # type: ignore
        assert filter_build["karaoke"]["monoLevel"] == 0.64  # type: ignore
        assert filter_build["karaoke"]["filterBand"] == 12.1  # type: ignore
        assert filter_build["karaoke"]["filterWidth"] == 3.2  # type: ignore
