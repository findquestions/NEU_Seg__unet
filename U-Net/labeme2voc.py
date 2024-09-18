#!/usr/bin/env python

from __future__ import print_function

import argparse
import glob
import os
import os.path as osp
import sys
import imgviz
import numpy as np
import PIL.Image

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('input_images', help='input directory with original images')
    parser.add_argument('input_masks', help='input directory with mask images')
    parser.add_argument('output_dir', help='output dataset directory')
    parser.add_argument('--labels', help='labels file', required=True)
    parser.add_argument(
        '--noviz', help='no visualization', action='store_true'
    )
    args = parser.parse_args()

    if osp.exists(args.output_dir):
        print('Output directory already exists:', args.output_dir)
        sys.exit(1)
    os.makedirs(args.output_dir)
    os.makedirs(osp.join(args.output_dir, 'JPEGImages'))
    os.makedirs(osp.join(args.output_dir, 'SegmentationClass'))
    os.makedirs(osp.join(args.output_dir, 'SegmentationClassPNG'))
    if not args.noviz:
        os.makedirs(
            osp.join(args.output_dir, 'SegmentationClassVisualization')
        )
    print('Creating dataset:', args.output_dir)

    class_names = []
    class_name_to_id = {}
    for i, line in enumerate(open(args.labels).readlines()):
        class_id = i - 1  # starts with -1
        class_name = line.strip()
        class_name_to_id[class_name] = class_id
        if class_id == -1:
            assert class_name == '__ignore__'
            continue
        elif class_id == 0:
            assert class_name == '_background_'
        class_names.append(class_name)
    class_names = tuple(class_names)
    print('class_names:', class_names)
    out_class_names_file = osp.join(args.output_dir, 'class_names.txt')
    with open(out_class_names_file, 'w') as f:
        f.writelines('\n'.join(class_names))
    print('Saved class_names:', out_class_names_file)

    for img_file in glob.glob(osp.join(args.input_images, '*.jpg')):  # Assuming original images are in .jpg format
        base = osp.splitext(osp.basename(img_file))[0]
        out_img_file = osp.join(args.output_dir, 'JPEGImages', base + '.jpg')
        out_lbl_file = osp.join(args.output_dir, 'SegmentationClass', base + '.npy')
        out_png_file = osp.join(args.output_dir, 'SegmentationClassPNG', base + '.png')
        if not args.noviz:
            out_viz_file = osp.join(
                args.output_dir,
                'SegmentationClassVisualization',
                base + '.jpg',
            )

        # Copy original image
        img = np.asarray(PIL.Image.open(img_file))
        PIL.Image.fromarray(img).save(out_img_file)

        # Process corresponding mask image
        mask_file = osp.join(args.input_masks, base + '.png')  # Assuming mask images are in .png format
        lbl = np.asarray(PIL.Image.open(mask_file), dtype=np.uint8)

        # Save mask as .npy file
        np.save(out_lbl_file, lbl)

        # Save mask as PNG file for visualization
        PIL.Image.fromarray(lbl).save(out_png_file)

        if not args.noviz:
            # Assuming `imgviz.label2rgb` does not require `img` parameter anymore
            viz = imgviz.label2rgb(
                label=lbl,
                label_names=class_names,
                font_size=15,
                loc='rb',
            )
            imgviz.io.imsave(out_viz_file, viz)


if __name__ == '__main__':
    main()
