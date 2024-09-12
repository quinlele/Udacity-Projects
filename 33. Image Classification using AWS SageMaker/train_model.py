#TODO: Import your dependencies.
#For instance, below are some dependencies you might need if you are using Pytorch
import numpy as np
import os
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

import argparse
import logging
import sys
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))



#TODO: Import dependencies for Debugging andd Profiling

def test(model, test_loader, criterion):
    '''
    TODO: Complete this function that can take a model and a 
          testing data loader and will get the test accuray/loss of the model
          Remember to include any debugging/profiling hooks that you might need
    '''
    model.eval()
    total_loss = 0
    total_acc = 0

    for data_input, label in test_loader:
        data_output = model(data_input)
        loss = criterion(data_output, label)
        pred = torch.argmax(data_output, 1)
        total_loss += loss.item()*data_input.size(0)
        total_acc += torch.sum(pred == label.data).item()

    total_loss /= len(test_loader.dataset)
    total_acc /= len(test_loader.dataset)

    logger.info(f"Testing Loss: {total_loss}")
    logger.info(f"Testing Accuracy: {total_acc}")


def train(model, train_loader, criterion, optimizer):
    '''
    TODO: Complete this function that can take a model and
          data loaders for training and will get train the model
          Remember to include any debugging/profiling hooks that you might need
    '''
    n_epochs = 10

    for epoch in range(n_epochs):
        model.train()
        epoch_loss = 0
        epoch_acc = 0
        n_samples = 0

        for data_input, label in train_loader:
            data_output = model(data_input)
            loss = criterion(data_output, label)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            pred = torch.argmax(data_output, 1)
            epoch_loss += loss.item()*data_input.size(0)
            epoch_acc += torch.sum(pred == label.data).item()
            n_samples += len(data_input)

        epoch_loss /= n_samples
        epoch_acc /= n_samples

        logger.info(f"Epoch {epoch}, loss: {epoch_loss}, epoch acc: {epoch_acc}")

    return model


def net():
    '''
    TODO: Complete this function that initializes your model
          Remember to use a pretrained model
    '''
    model = models.resnet50(pretrained=True)

    for param in model.parameters():
        param.requires_grad = False

    n_features = model.fc.in_features
    model.fc = nn.Sequential(
                   nn.Linear(n_features, 128),
                   nn.ReLU(inplace=True),
                   nn.Linear(128, 133))

    return model


def create_data_loaders(data, batch_size):
    '''
    This is an optional function that you may or may not need to implement
    depending on whether you need to use data loaders or not
    '''
    train_data_path = os.path.join(data, 'train')
    test_data_path = os.path.join(data, 'test')

    train_transform = transforms.Compose([
        transforms.RandomResizedCrop((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    test_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    train_data = torchvision.datasets.ImageFolder(
        root=train_data_path,
        transform=train_transform
    )
    train_data_loader = torch.utils.data.DataLoader(
        train_data,
        batch_size=batch_size,
        shuffle=True,
    )

    test_data = torchvision.datasets.ImageFolder(
        root=test_data_path,
        transform=test_transform
    )
    test_data_loader = torch.utils.data.DataLoader(
        test_data,
        batch_size=batch_size,
        shuffle=False,
    )

    return train_data_loader, test_data_loader


def main(args):
    logger.info(f'Learning rate: {args.learning_rate}, Batch size: {args.batch_size}')
    logger.info(f'Data Paths: {args.data}')
    '''
    TODO: Initialize a model by calling the net function
    '''
    model = net()
    
    '''
    TODO: Create your loss and optimizer
    '''
    criterion = nn.CrossEntropyLoss(ignore_index=133)
    optimizer = optim.Adam(model.fc.parameters(), lr=args.learning_rate)

    train_loader, test_loader = create_data_loaders(args.data, args.batch_size)
    
    '''
    TODO: Call the train function to start training your model
    Remember that you will need to set up a way to get training data from S3
    '''
    logger.info("Training the model")
    model = train(model, train_loader, criterion, optimizer)
    
    '''
    TODO: Test the model to see its accuracy
    '''
    logger.info("Testing the model")
    test(model, test_loader, criterion)
    
    '''
    TODO: Save the trained model
    '''
    logger.info("Saving the model")
    torch.save(model.state_dict(), os.path.join(args.model_dir, "model.pth"))


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    '''
    TODO: Specify any training args that you might need
    '''
    parser.add_argument('--learning-rate',
                        type=float,
                        default=0.01)
    parser.add_argument('--batch-size',
                        type=int,
                        default=32)
    parser.add_argument('--data', type=str,
                        default=os.environ['SM_CHANNEL_TRAINING'])
    parser.add_argument('--model_dir',
                        type=str,
                        default=os.environ['SM_MODEL_DIR'])
    parser.add_argument('--output_dir',
                        type=str,
                        default=os.environ['SM_OUTPUT_DATA_DIR'])
    
    args = parser.parse_args()
    
    main(args)