from trend import trend
from channels import channels

filepath = "../../../neutral-meson-spectra/" \
    "input-data/data/LHC16/trigger_qa/iteration2/LHC16g-pass1.root"


def main():
    trend(filepath)
    channels(filepath)


if __name__ == '__main__':
    main()
