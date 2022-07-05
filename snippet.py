#English + CNN based model as vision backbone

from ZSIClight import ZeroShotImageClassification

zsic = ZeroShotImageClassification()

pred = zsic(image=r"C:\Users\Samarth\Desktop\Clark Scholars\cow.jpg", candidate_labels=["cow","scooter"])

#print(pred)

'''
Prints the following
{'image': 'http://images.cocodataset.org/val2017/000000039769.jpg', 
'scores': [0.00046659182, 0.0024660423, 0.9949238, 0.002143612], 
'labels': ['birds', 'lions', 'cats', 'dogs']
}
'''
