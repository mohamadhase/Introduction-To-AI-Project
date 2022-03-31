from modules.Data import Data
from modules.FeatureEngineering import FeatureEngineering



def main():
    data = Data()
    print("Step 1 Done")

    featureEngineering = FeatureEngineering(data
    )
    print("Step 2 Done")

    featureEngineering.apply_dv1()

    print("Step 3 Done")

    featureEngineering.apply_dv2()
    print("Step 4 Done")


if __name__ == "__main__":
    main()