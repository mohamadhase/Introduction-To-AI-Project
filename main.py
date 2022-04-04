from modules.Data import Data
from modules.FeatureEngineering import FeatureEngineering



def main():
    data = Data()

    featureEngineering = FeatureEngineering(data)


if __name__ == "__main__":
    main()