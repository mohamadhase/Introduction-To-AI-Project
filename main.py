from modules.Data import Data
from modules.FeatureEngineering import FeatureEngineering



def main():
    data = Data()

    featureEngineering = FeatureEngineering(data)

    featureEngineering.apply_dv8()
    




if __name__ == "__main__":
    main()