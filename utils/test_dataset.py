from pointnet.my_dataset import MyDataset
from pointnet.dataset import ShapeNetDataset
from pointnet.model import PointNetCls
import torch

# root='/home/erfan/Personal/project/pointnet.pytorch/1bdf0a0bb9db1db68998b3b64a143d42.pts',

dataset = MyDataset(
    root='/home/erfan//Personal/project/webots/world1/controllers/pioneer_pc_controller/points.pts',
    classification=True,
    npoints=2500,
    split='test',
    data_augmentation=False
    )

model = PointNetCls(k=16)
model.load_state_dict(torch.load('./cls/cls_model_9.pth', map_location=torch.device('cpu')))
model.eval()


testdataloader = torch.utils.data.DataLoader(
        dataset,
        batch_size=1,
        shuffle=True,
        num_workers=1)

j, data = next(enumerate(testdataloader, 0))
points, target = data
# target = target[:, 0]
points = points.transpose(2, 1)
# points, target = points.cuda(), target.cuda()
model = model.eval()
pred, _, _ = model(points)
print(pred.data[0].sum().item() / pred.data[0][3].item())
pred_choice = pred.data.max(1)[1]
print(pred.data[0])

import csv
f = open('results/webots_pred.csv', 'a')
writer = csv.writer(f)
writer.writerow([
    'Car', 
    pred.data[0].sum().item() / pred.data[0][3].item(), 
    dataset.id2cat[int(pred_choice[0])]
])


print('its a: ', dataset.id2cat[int(pred_choice[0])])
