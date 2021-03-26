# UNDER CONSTRUCTION - IDEA IS TO HAVE ONE SCRIPT THAT HAS TWO COMMANDS:
# 1- PROJECT: LIKE EXISTING generate_labels.py (SUPPORTS LIST OF SAMPLE NAMES OR AUTO-GENERATED)
# 2- SPREADSHEET: PRINT LABELS WITH ANY ARBITRARY TEXT AND CODE (BOTH ARE DERIVED FROM SPREADSHEET AND DON'T HAVE TO BE THE SAME)

#!/usr/bin/env python

import click
import os
import math
import time
import numpy as np
import pandas as pd
import qrcode
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

# global variables
template_head = 'template_LCRY1700_head.tex'
template_tail = 'template_LCRY1700_tail.tex'
template_cols = 5

# @click.group()

def labelmaker():
    pass

def create_directory(project_name):

    # create directory for project_name labels
    newdir = 'labels_%s' % project_name
    if not os.path.exists(newdir):
        os.makedirs(newdir)

def generate_code_and_text():


def make_label(project_name, contact, sample_type, date, sample, replicate, num_replicates, label_width, label_height):

    # generate text code and qr code
    # longcode = '%s_%s_%s_%s_%s_%01d' % (project_name, contact, sample_type, date, sample, replicate)
    if (num_replicates > 1):
        code = '%s_%s_%01d' % (project_name, sample, replicate)
        string = 'Project:%s\nContact:%s\nType:%s\nDate:%s\nSample:%s\nReplicate:%01d' % (
            project_name, contact, sample_type, date, sample, replicate)
    else:
        code = '%s_%s' % (project_name, sample)
        string = 'Project:%s\nContact:%s\nType:%s\nDate:%s\nSample:%s' % (
            project_name, contact, sample_type, date, sample)

    # make qr code
    qr = qrcode.QRCode(
        #version=1, # set fit=True below to make this automatic
        error_correction=qrcode.constants.ERROR_CORRECT_L, # default is ERROR_CORRECT_M
        box_size=6, # number of pixels per box
        border=20, # larger border yields smaller qr code
    )
    qr.add_data(code)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # make label from qr code and string
    label = Image.new('RGB', (int(img.height*label_width/label_height), img.height), color='white')
    label.paste(img, (0,0))
    draw = ImageDraw.Draw(label)
    font = ImageFont.truetype('Monaco.dfont', 32)
    draw.text(((img.height * 0.85), int(img.height * 0.18)), string, (0,0,0), font=font)
    if (num_replicates > 1):
        label.save('labels_%s/label_%s_%01d.png' % (project_name, sample, replicate))
    else:
        label.save('labels_%s/label_%s.png' % (project_name, sample))


def make_sheet():


@labelmaker.command()
@click.option('--project_name', '-p', required=True, type=str,
              help="Short project name. Must not contain spaces.")
@click.option('--contact', '-c', required=True, type=str,
              help="Last name of point of contact. Must not contain spaces.")
@click.option('--sample_type', '-t', required=True, type=str,
              help="Type of sample (e.g. DNA/0.2um).")
@click.option('--date', '-d', required=True, type=str,
              help="Date (e.g. 2018-10-12).")
@click.option('--sample_list', '-l', required=False, type=click.Path(exists=True),
              help="List of samples. If none is provided, samples will be numbered 1 to num_samples.")
@click.option('--num_samples', '-s', required=False, type=int, default=5,
              help="Number of unique samples; ignored if sample_list provided. [default=5]")
@click.option('--num_replicates', '-r', required=False, type=int, default=1,
              help="Number of replicates per sample. [default=1 (i.e. no replicates)]")
@click.option('--label_width', '-w', required=False, type=float, default=1.05,
              help="Width of label in inches. 1.05 works for 1.28in labels. [default=1.05]")
@click.option('--label_height', '-h', required=False, type=float, default=0.5,
              help="Height of label in inches. 0.5 works for 0.5in labels. [default=0.5]")

def project(project_name, contact, sample_type, date, sample_list, num_samples, num_replicates, label_width, label_height):

    create_directory(project_name)

    # read sample list (and count number of samples) or number from 1 to num_samples
    if (sample_list):
        with open(sample_list, 'r') as f:
            samples = [line.rstrip() for line in f.readlines()]
            num_samples = len(samples)
    else:
        samples = [str(x).zfill(int(np.ceil(np.log10(num_samples+1)))) for x in np.arange(num_samples)+1]

    # make labels and latex table, iterating over sample numbers and replicates
    tex_table = {}
    num_sheets = math.ceil(num_samples * num_replicates / 85)
    for sheet in range(1, num_sheets + 1):
        tex_table[sheet] = ''
    tex_counter = 0
    for sample in samples:
        for replicate in np.arange(num_replicates) + 1:
            tex_counter += 1
            this_sheet = math.ceil(tex_counter / 85)
            make_label(project_name, contact, sample_type, date, sample, replicate, num_replicates, label_width, label_height)
            if (num_replicates > 1):
                tex_table[this_sheet] += '\\includegraphics[width=\\w]{label_%s_%01d} & ' % (sample, replicate)
            else:
                tex_table[this_sheet] += '\\includegraphics[width=\\w]{label_%s} & ' % sample
            if ((tex_counter % template_cols) == 0):
                tex_table[this_sheet] = tex_table[this_sheet][:-2]
                tex_table[this_sheet] += '\\\\[\\h]\n'

    # make labelsheet latex file
    time.sleep(3)
    with open(template_head, 'r') as f:
        head = f.read()
    with open(template_tail, 'r') as f:
        tail = f.read()
    for sheet in range(1, num_sheets + 1):
        with open(f'labels_{project_name}/labelsheet{sheet}_{project_name}_LCRY1700.tex', 'w') as t:
            t.write(head)
            t.write(tex_table[sheet])
            t.write(tail)

@labelmaker.command()
@click.option('--spreadsheet', '-f', required=True, type=click.Path(exists=True),
              help="Spreadsheet containing codes and text to print on labels. Valid file types (auto-detected): .csv, .xls, .xlsx.")
@click.option('--header/--no-header', default=True,
              help="Whether spreadsheet has a header column (default) or not.")
@click.option('--code_column', '-c', required=False, type=int, default=0,
              help="Counting from zero, column containing text to encode as QR code (default: 0, ie first column).")
@click.option('--text_column', '-t', required=False, type=int, default=1,
              help="Counting from zero, column containing text to print next to QR code (default: 1, ie second column).")
@click.option('--label_width', '-w', required=False, type=float, default=1.05,
              help="Width of label in inches. 1.05 works for 1.28in labels. [default=1.05]")
@click.option('--label_height', '-h', required=False, type=float, default=0.5,
              help="Height of label in inches. 0.5 works for 0.5in labels. [default=0.5]")

def spreadsheet(project_name, contact, sample_type, date, sample_list, num_samples, num_replicates, label_width, label_height):

    create_directory(project_name)

    # read sample list (and count number of samples) or number from 1 to num_samples
    if (sample_list):
        with open(sample_list, 'r') as f:
            samples = [line.rstrip() for line in f.readlines()]
            num_samples = len(samples)
    else:
        samples = [str(x).zfill(int(np.ceil(np.log10(num_samples+1)))) for x in np.arange(num_samples)+1]

    # make labels and latex table, iterating over sample numbers and replicates
    tex_table = {}
    num_sheets = math.ceil(num_samples * num_replicates / 85)
    for sheet in range(1, num_sheets + 1):
        tex_table[sheet] = ''
    tex_counter = 0
    for sample in samples:
        for replicate in np.arange(num_replicates) + 1:
            tex_counter += 1
            this_sheet = math.ceil(tex_counter / 85)
            make_label(project_name, contact, sample_type, date, sample, replicate, num_replicates, label_width, label_height)
            if (num_replicates > 1):
                tex_table[this_sheet] += '\\includegraphics[width=\\w]{label_%s_%01d} & ' % (sample, replicate)
            else:
                tex_table[this_sheet] += '\\includegraphics[width=\\w]{label_%s} & ' % sample
            if ((tex_counter % template_cols) == 0):
                tex_table[this_sheet] = tex_table[this_sheet][:-2]
                tex_table[this_sheet] += '\\\\[\\h]\n'

    # make labelsheet latex file
    time.sleep(3)
    with open(template_head, 'r') as f:
        head = f.read()
    with open(template_tail, 'r') as f:
        tail = f.read()
    for sheet in range(1, num_sheets + 1):
        with open(f'labels_{project_name}/labelsheet{sheet}_{project_name}_LCRY1700.tex', 'w') as t:
            t.write(head)
            t.write(tex_table[sheet])
            t.write(tail)

if __name__ == "__main__":
    labelmaker()
