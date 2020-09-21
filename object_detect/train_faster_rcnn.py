""" Script by Johannes B. Reiche, inspired by: https://pytorch.org/tutorials/intermediate/torchvision_tutorial.html """
import torchvision
from torch.utils import data
import os, pickle
import numpy as np
#from data_import.data_loader import DataLoader
import torch
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from semantic_segmentation.DeepLabV3.utils import ext_transforms as et
from object_detect.leather_data import LeatherData_BB
from object_detect.helper.engine2 import train_one_epoch, evaluate
import object_detect.helper.utils as utils

def init_model(num_classes):
    #load a model pre-trained pre-trained on COCO
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
    # replace the classifier with a new one, that has
    # num_classes which is user-defined
    num_classes = num_classes  # 1 class (person) + background
    # get number of input features for the classifier
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    # replace the pre-trained head with a new one
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    return model

transform_function = et.ExtCompose([et.ExtEnhanceContrast(),et.ExtScale(256),et.ExtToTensor(),
                                    et.ExtNormalize(mean=[0.485, 0.456, 0.406],
                                    std=[0.229, 0.224, 0.225])])

if __name__ == '__main__':

    device = torch.device('cpu')
    #device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    print("Device: %s" % device)

    model = init_model(num_classes=2)
    model.to(device)

    # construct an optimizer
    params = [p for p in model.parameters() if p.requires_grad]
    params_to_train = params[64:]
    optimizer = torch.optim.SGD(params_to_train, lr=0.005,
                                momentum=0.9, weight_decay=0.0005)

    # and a learning rate scheduler which decreases the learning rate by
    # 10x every 3 epochs
    lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer,
                                                   step_size=3,
                                                   gamma=0.1)

    num_epoch = 2
    print_freq = 10

    path_mask = r'C:\Users\johan\OneDrive\Skrivebord\leather_patches\mask'
    path_img = r'C:\Users\johan\OneDrive\Skrivebord\leather_patches\img'

    batch_size = 16
    val_batch_size = 4

    visibility_scores = [3]

    if type(visibility_scores) == list:
        with open(
                r'C:\Users\johan\iCloudDrive\DTU\KID\BA\Kode\Bachelor-Criterion-AI\semantic_segmentation\DeepLabV3\outfile.jpg',
                'rb') as fp:
            itemlist = np.array(pickle.load(fp))

    file_names = np.array([img[:-4] for img in os.listdir(path_img)])
    itemlist=itemlist[file_names.astype(np.uint8)]
    file_names=np.sort(file_names)[np.logical_or(itemlist==2, itemlist==3)]
    N_files=len(file_names)
    shuffled_index=np.random.permutation(len(file_names))
    file_names_img=file_names[shuffled_index]
    file_names=file_names[file_names != ".DS_S"]

    # Define dataloaders
    train_dst = LeatherData_BB(path_mask=path_mask,path_img=path_img,list_of_filenames=file_names[:210],transform=transform_function)
    val_dst = LeatherData_BB(path_mask=path_mask,path_img=path_img,list_of_filenames=file_names[210:],transform=transform_function)

    train_loader = data.DataLoader(
       train_dst, batch_size=batch_size, shuffle=True, num_workers=2, collate_fn=utils.collate_fn)
    val_loader = data.DataLoader(
        val_dst, batch_size=val_batch_size, shuffle=False, num_workers=2, collate_fn=utils.collate_fn)
    print("Train set: %d, Val set: %d" % (len(train_dst), len(val_dst)))

    for epoch in range(num_epoch):
        print("About to train")
        # train for one epoch, printing every 10 iterations
        train_one_epoch(model, optimizer, train_loader, device, epoch,print_freq=10)
        # update the learning rate
        lr_scheduler.step()
        print("\n Finished training for epoch!")
        # evaluate on the test dataset
        evaluate(model, val_loader, device=device)
        print("\n Finished evaluation for epoch!")