#!/usr/bin/env python

import click
import os
import numpy as np
import pandas as pd
import qrcode
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

def create_directory(project):

    # create directory for project labels
    newdir = 'labels_%s' % project
    if not os.path.exists(newdir):
        os.makedirs(newdir)

def make_label(project, contact, sample_type, date, sample, replicate, label_width, label_height):

    # generate text code and qr code
    code = '%s_%s_%s_%s_s%03d_r%02d' % (project, contact, sample_type, date, sample, replicate)
    string = 'Project:%s\nContact:%s\nType:%s\nDate:%s\nSampleID:s%03d ________\nReplicate:r%02d' % (
        project, contact, sample_type, date, sample, replicate)

    # make qr code
    qr = qrcode.QRCode(
        #version=1, # set fit=True below to make this automatic
        #error_correction=qrcode.constants.ERROR_CORRECT_L, # default is ERROR_CORRECT_M
        box_size=6, # number of pixels per box
        border=12, # larger border yields smaller qr code
    )
    qr.add_data(code)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # make label from qr code and string
    label = Image.new('RGB', (int(img.height*label_width/label_height), img.height), color='white')
    label.paste(img, (0,0))
    draw = ImageDraw.Draw(label)
    font = ImageFont.truetype('Monaco.dfont', 32)
    draw.text(((img.height*0.85), int(img.height*0.18)), string, (0,0,0), font=font)
    label.save('labels_%s/label_s%03d_r%02d.png' % (project, sample, replicate))

@click.command()
@click.option('--project', '-p', required=True, type=str,
              help="Short project name. Must not contain spaces.")
@click.option('--contact', '-c', required=True, type=str,
              help="Last name of point of contact. Must not contain spaces.")
@click.option('--sample_type', '-t', required=True, type=str,
              help="Type of sample (eg DNA.2um). Must not contain spaces.")
@click.option('--date', '-d', required=True, type=int,
              help="Date as YYYYMMDD or YYYYMM.")
@click.option('--num_samples', '-s', required=True, type=int,
              help="Number of unique samples.")
@click.option('--num_replicates', '-r', required=True, type=int,
              help="Number of replicates per sample.")
@click.option('--label_width', '-w', required=True, type=float,
              help="Width of label in inches.")
@click.option('--label_height', '-h', required=True, type=float,
              help="Height of label in inches.")

def main(project, contact, sample_type, date, num_samples, num_replicates, label_width, label_height):

    create_directory(project)

    # make labels, iterating over sample numbers and replicates
    for sample in np.arange(num_samples)+1:
        for replicate in np.arange(num_replicates)+1:
            make_label(project, contact, sample_type, date, sample, replicate, label_width, label_height)

if __name__ == "__main__":
    main()
