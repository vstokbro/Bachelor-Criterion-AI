dataloader=DataLoader(data_path='/Users/villadsstokbro/Dokumenter/DTU/KID/5. Semester/Bachelor /leather_patches',metadata_path = r'samples/model_comparison.csv')
import_data_and_mask_classifier(dataloader,good_patches=True,visibility_scores=[2,3],directory_path='/Users/villadsstokbro/Dokumenter/DTU/KID/5. Semester/Bachelor /data_folder/cropped_data')