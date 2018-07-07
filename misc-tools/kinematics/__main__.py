from generator.generator import Analysis
from generator.generator import AngleSelection


def main():
    angle_distribution = AngleSelection()
    Analysis().transform(
        [angle_distribution]
    )
    angle_distribution.write()


if __name__ == '__main__':
    main()
