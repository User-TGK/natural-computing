import random


def classify(z: list[float]) -> int:
    if (z[0] >= 0.7) or ((z[0] <= 0.3) and (z[1] >= (-0.2 - z[0]))):
        return 1

    return 0


def main():
    # generate the Artificial dataset 1 (400 data vectors with z1,z2~U(-1,1))

    with open('artificial1.data', 'w') as f:
        for _ in range(400):
            z = [random.uniform(-1, 1), random.uniform(-1, 1)]
            c = classify(z)
            f.write(f'{z[0]},{z[1]},{c}\n')


if __name__ == '__main__':
    main()
