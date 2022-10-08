# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
"""
Run YOLOv5 detection inference on images, videos, directories, globs, YouTube, webcam, streams, etc.

Usage - sources:
    $ python detect.py --weights yolov5s.pt --source 0                               # webcam
                                                     img.jpg                         # image
                                                     vid.mp4                         # video
                                                     path/                           # directory
                                                     'path/*.jpg'                    # glob
                                                     'https://youtu.be/Zgi9g1ksQHc'  # YouTube
                                                     'rtsp://example.com/media.mp4'  # RTSP, RTMP, HTTP stream

Usage - formats:
    $ python detect.py --weights yolov5s.pt                 # PyTorch
                                 yolov5s.torchscript        # TorchScript
                                 yolov5s.onnx               # ONNX Runtime or OpenCV DNN with --dnn
                                 yolov5s.xml                # OpenVINO
                                 yolov5s.engine             # TensorRT
                                 yolov5s.mlmodel            # CoreML (macOS-only)
                                 yolov5s_saved_model        # TensorFlow SavedModel
                                 yolov5s.pb                 # TensorFlow GraphDef
                                 yolov5s.tflite             # TensorFlow Lite
                                 yolov5s_edgetpu.tflite     # TensorFlow Edge TPU
                                 yolov5s_paddle_model       # PaddlePaddle
"""

import argparse
import os
import platform
import sys
from pathlib import Path
import time
import torch
from cv2 import *

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from models.common import DetectMultiBackend
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadScreenshots, LoadStreams
from utils.general import (LOGGER, Profile, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_boxes, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, smart_inference_mode




@smart_inference_mode()
def run(
        weights=ROOT / 'yolov5s.pt',  # model path or triton URL
        source=ROOT / 'data/images',  # file/dir/URL/glob/screen/0(webcam)
        data=ROOT / 'data/coco128.yaml',  # dataset.yaml path
        imgsz=(640, 640),  # inference size (height, width)
        conf_thres=0.25,  # confidence threshold
        iou_thres=0.45,  # NMS IOU threshold
        max_det=1000,  # maximum detections per image
        device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        view_img=False,  # show results
        save_txt=False,  # save results to *.txt
        save_conf=False,  # save confidences in --save-txt labels
        save_crop=False,  # save cropped prediction boxes
        nosave=False,  # do not save images/videos
        classes=None,  # filter by class: --class 0, or --class 0 2 3
        agnostic_nms=False,  # class-agnostic NMS
        augment=False,  # augmented inference
        visualize=False,  # visualize features
        update=False,  # update all models
        project=ROOT / 'runs/detect',  # save results to project/name
        name='exp',  # save results to project/name
        exist_ok=False,  # existing project/name ok, do not increment
        line_thickness=3,  # bounding box thickness (pixels)
        hide_labels=False,  # hide labels
        hide_conf=False,  # hide confidences
        half=False,  # use FP16 half-precision inference
        dnn=False,  # use OpenCV DNN for ONNX inference
        vid_stride=1,  # video frame-rate stride
):

    # PREPARING TARNEEB
    order = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    winner = "__"
    cards_list = set()
    trnb_set = set()
    trnb_list = []

    def card_number(elem):
        return elem[:-1]

    def card_type(elem):
        return elem[-1]

    def get_index(elem):
        return order.index(card_number(elem))

    def check_card(card):
        full_time = 0
        var = f"{s}{'' if len(det) else '(no detections), '}{dt[1].dt * 1E3:.1f}ms"
        full_time += float(var[17:21])
        if full_time >= 2000:
            return True


    trnb = 'D'

    unique_cards = set()
    first, second, third, fourth = '','','',''

    font = cv2.FONT_HERSHEY_TRIPLEX
    thick = 3
    color = (255,255,255)
    

    source = str(source)
    save_img = not nosave and not source.endswith('.txt')  # save inference images
    is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
    is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
    webcam = source.isnumeric() or source.endswith('.txt') or (is_url and not is_file)
    screenshot = source.lower().startswith('screen')
    if is_url and is_file:
        source = check_file(source)  # download

    # Directories
    save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

    # Load model
    device = select_device(device)
    model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # check image size

    # Dataloader
    bs = 1  # batch_size
    if webcam:
        view_img = check_imshow()
        dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
        bs = len(dataset)
    elif screenshot:
        dataset = LoadScreenshots(source, img_size=imgsz, stride=stride, auto=pt)
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
    vid_path, vid_writer = [None] * bs, [None] * bs

    # Run inference
    model.warmup(imgsz=(1 if pt or model.triton else bs, 3, *imgsz))  # warmup
    seen, windows, dt = 0, [], (Profile(), Profile(), Profile())
    for path, im, im0s, vid_cap, s in dataset:
        with dt[0]:
            im = torch.from_numpy(im).to(model.device)
            im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
            im /= 255  # 0 - 255 to 0.0 - 1.0
            if len(im.shape) == 3:
                im = im[None]  # expand for batch dim

        # Inference
        with dt[1]:
            visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
            pred = model(im, augment=augment, visualize=visualize)

        # NMS
        with dt[2]:
            pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

        # Second-stage classifier (optional)
        # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)

        # Process predictions
        for i, det in enumerate(pred):  # per image
            seen += 1
            if webcam:  # batch_size >= 1
                p, im0, frame = path[i], im0s[i].copy(), dataset.count
                s += f'{i}: '
            else:
                p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)

            p = Path(p)  # to Path
            save_path = str(save_dir / p.name)  # im.jpg
            txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # im.txt
            s += '%gx%g ' % im.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            imc = im0.copy() if save_crop else im0  # for save_crop
            annotator = Annotator(im0, line_width=line_thickness, example=str(names))
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, 5].unique():
                    n = (det[:, 5] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}, "  # add to string

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    if save_txt:  # Write to file
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
                        with open(f'{txt_path}.txt', 'a') as f:
                            f.write(('%g ' * len(line)).rstrip() % line + '\n')

                    if save_img or save_crop or view_img:  # Add bbox to image
                        c = int(cls)  # integer class
                        label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                        annotator.box_label(xyxy, label, color=colors(c, True))
                    if save_crop:
                        save_one_box(xyxy, imc, file=save_dir / 'crops' / names[c] / f'{p.stem}.jpg', BGR=True)

            # Stream results
            im0 = annotator.result()
            if view_img:
                if platform.system() == 'Linux' and p not in windows:
                    windows.append(p)
                    cv2.namedWindow(str(p), cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # allow window resize (Linux)
                    cv2.resizeWindow(str(p), im0.shape[1], im0.shape[0])

                if winner: 
                    cv2.rectangle(im0, (50,25), (400,100), (0,0,0), -1)
                    cv2.putText(im0, f"Winner IS: {winner}", (80,70), font, 1, color, thick, cv2.LINE_4)
                    cv2.imshow(str(p), im0)
                    
                if first:
                    cv2.putText(im0, f"First Player: {first}", (70,150), font, 1, color, thick, cv2.LINE_4)
                    cv2.imshow(str(p), im0)

                if second:
                    cv2.putText(im0, f"Second Player: {second}", (70,200), font, 1, color, thick, cv2.LINE_4)
                    cv2.imshow(str(p), im0)

                if third:
                    cv2.putText(im0, f"Third Player: {third}", (70,250), font, 1, color, thick, cv2.LINE_4)
                    cv2.imshow(str(p), im0)

                
                if fourth:
                    cv2.putText(im0, f"Fourth Player: {fourth}", (70,300), font, 1, color, thick, cv2.LINE_4)
                    cv2.imshow(str(p), im0)                
                 
                cv2.imshow(str(p), im0)
                cv2.waitKey(5)  # 1 millisecond




            # Save results (image with detections)
            if save_img:
                if dataset.mode == 'image':
                    cv2.imwrite(save_path, im0)
                else:  # 'video' or 'stream'
                    if vid_path[i] != save_path:  # new video
                        vid_path[i] = save_path
                        if isinstance(vid_writer[i], cv2.VideoWriter):
                            vid_writer[i].release()  # release previous video writer
                        if vid_cap:  # video
                            fps = vid_cap.get(cv2.CAP_PROP_FPS)
                            w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                            h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        else:  # stream
                            fps, w, h = 55, im0.shape[1], im0.shape[0]
                        save_path = str(Path(save_path).with_suffix('.mp4'))  # force *.mp4 suffix on results videos
                        vid_writer[i] = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))

                    

                    vid_writer[i].write(im0)

        # Print time (inference-only)
        LOGGER.info(f"{s}{'' if len(det) else '(no detections), '}{dt[1].dt * 1E3:.1f}ms")


        # Writing on Screen the Detections
        ans = s[11: -1]
        S, C, D, H = [], [], [], []
        add = 0
        if ans :
            ans_list = ans.strip().split(',')[:-1]
            for pred in ans_list:
                if pred:
                    if len(pred.split()) == 2 and pred.split()[0] == '3':
                        add += 1
                    elif len(pred.split()) == 2 and pred.split()[0] == '4':
                        add += 1

            if ans_list != [' ']:
                final_list = [item.split()[-1] for item in ans_list]

            for item in final_list:
                
                num = item[:-1]
                typ = item[-1]

                if typ.upper() == 'S':
                    S.append(num)
                if typ.upper() == 'C':
                    C.append(num)
                if typ.upper() == 'D':
                    D.append(num)
                if typ.upper() == 'H':
                    H.append(num)
        
        else:
            final_list = []


        # Tarneeeb 
        if final_list:

            for card in final_list:
                if card not in unique_cards:
                    
                    if check_card(card):
                        print("HWWWWWWWYYYY")
                    unique_cards.add(card)

                    if not first:
                        first = card
                        game_type = card_type(first).upper()    
 
                    if not second and card != first:
                        second = card
                    if not third and card != first and card != second:
                        third = card

                    if not fourth and card != first and card != second and card != third:
                        fourth = card

                    if first and second and third and fourth:
                        break

                if first:
                    first = first.upper()
                    print("First: ", first)
                    cards_list.add(first)
                    if len(cards_list) == 1:

                        winner = 'First'

                    print("Winner 1: ", winner)
               
                # ---------------- Second ----------------------
                if second: 
                    second = second.upper()
                    print("Second: ", second)
                    cards_list.add(second)

                    if len(cards_list) == 2:
                        if card_type(second) == game_type:
                            if get_index(second) > get_index(first):
                                winner = "Second"

                        else:

                            if card_type(second).lower() == trnb.lower():

                                if second not in trnb_list:
                                    trnb_list.append(second)

                                if len(trnb_list) == 1:
                                    winner = "Second"
            
                    print("Winner 2: ", winner)
                # ---------------- Third ----------------------        
                if third:
                    third = third.upper()
                    print("Third: ", third)
                    cards_list.add(third)


                    if len(cards_list) == 3:


                        if len(trnb_list) == 1:

                            if card_type(third).lower() == trnb.lower():
                                if third not in trnb_list:
                                    trnb_list.append(third)

                                if get_index(third) > get_index(trnb_list[0]):
                                    winner ='Third'


                        else:

                            if card_type(third) == game_type:

                                if (get_index(third) > get_index(second)) and (get_index(third) > get_index(first)):
                                    winner = "Third"        

                            elif card_type(third).lower() == trnb.lower():
                                if third not in trnb_list:
                                    trnb_list.append(third)
                                winner = 'Third'

                
                    print("Winner 3: ", winner)
                # ---------------- Fourth ----------------------
                if fourth:
                    fourth = fourth.upper()
                    print("Fourth: ", fourth)
                    cards_list.add(fourth)

                            
                    if len(cards_list) == 4:
                        
                        if len(trnb_list) == 1 :

                            if card_type(fourth).lower() == trnb.lower():
                                if fourth not in trnb_list:
                                    trnb_list.append(fourth)                                
                                

                                if get_index(fourth) > get_index(trnb_list[0]):
                                    winner = 'Fourth'

                        elif len(trnb_list) == 2:

                            if card_type(fourth).lower() == trnb.lower():
                                if fourth not in trnb_list:
                                    trnb_list.append(fourth)

                                if (get_index(fourth) > get_index(trnb_list[0])) and (get_index(fourth) > get_index(trnb_list[1])):
                                    winner = 'Fourth'

                        else:

                            if card_type(fourth) == game_type:

                                if (get_index(fourth) > get_index(third)) and (get_index(fourth) > get_index(second)) and (get_index(fourth) > get_index(first)):
                                    winner = "Fourth"        

                            elif card_type(fourth).lower() == trnb.lower():
                                if fourth not in trnb_list:
                                    trnb_list.append(fourth)
                                winner = 'Fourth'            

                    print("Winner Final: ", winner)






    # Print results
    t = tuple(x.t / seen * 1E3 for x in dt)  # speeds per image
    LOGGER.info(f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS per image at shape {(1, 3, *imgsz)}' % t)
    if save_txt or save_img:
        s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
        LOGGER.info(f"Results saved to {colorstr('bold', save_dir)}{s}")
    if update:
        strip_optimizer(weights[0])  # update model (to fix SourceChangeWarning)


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default=ROOT / 'yolov5s.pt', help='model path or triton URL')
    parser.add_argument('--source', type=str, default=ROOT / 'data/images', help='file/dir/URL/glob/screen/0(webcam)')
    parser.add_argument('--data', type=str, default=ROOT / 'data/coco128.yaml', help='(optional) dataset.yaml path')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
    parser.add_argument('--max-det', type=int, default=1000, help='maximum detections per image')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='show results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--save-crop', action='store_true', help='save cropped prediction boxes')
    parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --classes 0, or --classes 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--visualize', action='store_true', help='visualize features')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default=ROOT / 'runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    parser.add_argument('--line-thickness', default=3, type=int, help='bounding box thickness (pixels)')
    parser.add_argument('--hide-labels', default=False, action='store_true', help='hide labels')
    parser.add_argument('--hide-conf', default=False, action='store_true', help='hide confidences')
    parser.add_argument('--half', action='store_true', help='use FP16 half-precision inference')
    parser.add_argument('--dnn', action='store_true', help='use OpenCV DNN for ONNX inference')
    parser.add_argument('--vid-stride', type=int, default=1, help='video frame-rate stride')
    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
    print_args(vars(opt))
    return opt


def main(opt):
    check_requirements(exclude=('tensorboard', 'thop'))
    run(**vars(opt))


if __name__ == "_main_":
    opt = parse_opt()
    main(opt)