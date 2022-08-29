import argparse
import torch
import torch.nn.parallel
import torch.utils.data
from torch.autograd import Variable
from pointnet.dataset import ShapeNetDataset
from pointnet.model import PointNetCls
import torch.nn.functional as F


#showpoints(np.random.randn(2500,3), c1 = np.random.uniform(0,1,size = (2500)))

parser = argparse.ArgumentParser()

parser.add_argument('--model', type=str, default = '',  help='model path')
parser.add_argument('--num_points', type=int, default=2500, help='input batch size')


opt = parser.parse_args()
print(opt)

import os
import csv

if not os.path.exists('results'):
    os.makedirs('results/')
f = open('./results/test_result_per_class.csv', 'w')
writer = csv.writer(f)
writer.writerow(['class', 'loss', 'accuracy'])

classes = [
            'Airplane',
            'Bag',
            'Cap',
            'Car', 
            'Chair', 
            'Earphone', 
            'Guitar',
            'Knife',
            'Lamp',
            'Laptop',
            'Motorbike', 
            'Mug',
            'Pistol', 
            'Rocket', 
            'Skateboard', 
            'Table',
]


for c in classes:
    test_dataset = ShapeNetDataset(
    root='./../shapenetcore_partanno_segmentation_benchmark_v0',
    split='test',
    classification=True,
    npoints=opt.num_points,
    data_augmentation=False,
    class_choice=c,
    )

    testdataloader = torch.utils.data.DataLoader(
        test_dataset, 
        batch_size=32, 
        shuffle=True
    )

    classifier = PointNetCls(k=len(test_dataset.classes))
    classifier.cuda()
    classifier.load_state_dict(torch.load(opt.model))
    classifier.eval()


    mean_loss = 0
    mean_accu = 0
    t = 0

    for i, data in enumerate(testdataloader, 0):
        points, target = data
        points, target = Variable(points), Variable(target[:, 0])
        points = points.transpose(2, 1)
        points, target = points.cuda(), target.cuda()
        pred, _, _ = classifier(points)
        loss = F.nll_loss(pred, target)

        pred_choice = pred.data.max(1)[1]
        correct = pred_choice.eq(target.data).cpu().sum()
        print('i:%d  loss: %f accuracy: %f' % (i, loss.data.item(), correct / float(32)))
        accu = (correct / float(32)).item()
        
        mean_loss += loss.data.item()
        mean_accu += accu
        t = i+1

    writer.writerow([c, mean_loss / t, mean_accu / t])

f.close()

