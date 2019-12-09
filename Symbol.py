# -*- coding: utf8 -*-
import numpy as np
import cv2
import random
import os
def color(imag, colors):
    global img, im, height, width
    img = cv2.resize(imag, (900, 600))
    im = img.copy()
    height, width = img.shape[:2]
    gray = grays(im)
    im_bin = binar(gray)
    for x in range(0, width):
        for y in range(0, height):
            if colors == 1:
                if img[y][x][1] > 50 and img[y][x][0] < 50 and img[y][x][2] < 50: # img[y][x][1] > 0 and img[y][x][0] < 10 and img[y][x][2] < 180: ########## if img[y][x][1] > 50 and img[y][x][0] < 50 and img[y][x][2] < 50
                    im_bin[y][x] = 1
                else:
                    im_bin[y][x] = 0
            elif colors == 0:
                if img[y][x][2] > 105 and img[y][x][1] < 100 and img[y][x][0] < 100: # if img[y][x][2] > 105 and img[y][x][1] < 100 and img[y][x][0] < 100:
                    im_bin[y][x] = 1
                else:
                    im_bin[y][x] = 0
            elif colors == 2:
                if img[y][x][0] > 90 and img[y][x][2] < 100 and img[y][x][1] < 100: # if img[y][x][0] > 90 and img[y][x][2] < 100 and img[y][x][1] < 100:
                    im_bin[y][x] = 1
                else:
                    im_bin[y][x] = 0
    im_bw = im_bin
    return im_bw
def grays(img):
    gray = (np.dot(img[..., :3], [0.299, 0.587, 0.114]))
    gray = gray.astype(np.uint8)
    return gray
def binar(gray):
    im_bw = gray.copy()
    height, width = gray.shape[:2]
    for x in range(0, width):
        for y in range(0, height):
            if gray[y][x] < 128:
                im_bw[y][x] = 0
            else:
                im_bw[y][x] = 255
    im_bw = (im_bw/255)
    return im_bw
def check(etalon, imag, accur, p):
    global height, width
    if p == 1:
        etalon = grays(etalon)
        etalon = binar(etalon)
    height, width = etalon.shape[:2]
    k = 0
    for x in range(0, width):
        for y in range(0, height):
            if imag[y][x] == etalon[y][x]:
                k += 1
    sum = height*width
    accur = 1 + (1 - (accur/10))
    if k < sum/accur:
        q = 0
    else:
        q = 1
    return q
def bound(im_bw):
    height, width = im_bw.shape[:2]
    i, j = 0, 0
    for x in range(0, width-2):
        for y in range(0, height-2):
            if (im_bw[y][x] == 1 and im_bw[y][x+1] == 1 and im_bw[y][x+2] == 1) or (im_bw[y][x] == 1 and im_bw[y][x-1] == 1 and im_bw[y][x-2] == 1):
                if i == 0:
                    a,b = x, y
                    i += 1
                a1, b1 = x, y
    for y in range(0, height-2):
        for x in range(0, width-2):
            if (im_bw[y][x] == 1 and im_bw[y+1][x] == 1 and im_bw[y+2][x] == 1) or (im_bw[y][x] == 1 and im_bw[y-1][x] == 1 and im_bw[y-2][x] == 1):
                if j == 0:
                    aa,bb = x, y
                    j += 1
                aa1, bb1 = x, y
    return a, bb, a1, bb1
def imagine(opens):
    img = cv2.imread('{}'.format(opens))
    img = cv2.resize(img, (900, 600))
    return img
def general(im_bw, accur):
    alph = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    result = bound(im_bw)
    a, bb, a1, bb1 = result[0], result[1], result[2], result[3]
    crop = im_bw[bb:bb1, a:a1]
    crop = cv2.resize(crop, (200, 250))
    i = 0
    flag = 0
    while i < len(alph):
        if i < 10 and flag == 0:
            etalon = (cv2.imread('Gen/{}.jpg'.format(i)))
        elif i >= 10 and flag == 0:
            flag = 1
            i = 0
        if flag == 1:
            etalon = (cv2.imread('Gen/{}.jpg'.format(alph[i])))
        q = check(etalon, crop, accur, p = 1)
        if q == 1:
            if flag == 0:
                print('Оригинал =>', i)
                text = 'Original=>{}'.format(i)
            elif flag == 1:
                print('Оригинал =>', alph[i])
                text = 'Original=>{}'.format(alph[i])
            break
        i += 1
    if q == 0:
        etalon = np.zeros((250,200,3), np.uint8)
        cv2.putText(etalon, "Not found", (20, etalon.shape[0]//2), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
        print('Оригинал не найден')
        text = 'Not found'
    if (a1+etalon.shape[1]+100) < img.shape[1] and (bb1-100-etalon.shape[0]) > 0:
        cv2.line(img, (a, bb-5), (a1+100, bb1-100-etalon.shape[0]), (255, 0, 0), 5)
        cv2.line(img, (a1+5, bb1), (a1+etalon.shape[1]+100, bb1-100), (255, 0, 0), 5)
        cv2.line(img, (a1+5, bb1-50), (a1+100, bb1-100), (255, 0, 0), 5) # a, bb1
        cv2.line(img, (a1, bb-5), (a1+etalon.shape[1]+100, bb1-100-etalon.shape[0]), (255, 0, 0), 5)
        cv2.rectangle(img,(a1+100, bb1-100-etalon.shape[0]),(a1+etalon.shape[1]+100, bb1-100),(255,0,0),20)
        i, j = 0, 0
        for x in range(a1+100, a1+etalon.shape[1]+100):
            for y in range(bb1-100-etalon.shape[0], bb1-100):
                img[y][x] = etalon[j][i]
                j += 1
                if j == etalon.shape[0]:
                    i += 1
                    j = 0
                if i == etalon.shape[1]:
                    break
    cv2.rectangle(img,(a-5,bb-5),(a1+5,bb1+5),(0,0,255),5)
    cv2.putText(img, text, (0, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 10)
    return img
def filt(output, quant, colors):
    im_bw = color(output, colors)
    img = im_bw.copy()
    if quant == 0:
        return img
    height, width = img.shape[:2]
    i = 1
    while i <= quant:
        r = 0
        while r <= 5:
            try:
                for x in range(0, width-r):
                    for y in range(0, height-r):
                        if x == width-1 or y == height-1:
                            img[y][x] = 0
                        if img[y][x] == 1 and im_bw[y-i][x] == 0 and im_bw[y+i][x] == 0 and im_bw[y][x-i] == 0 and im_bw[y][x+i] == 0:
                            img[y][x] = 0
                for x in range(0, width-r):
                    for y in range(0, height-r):
                        if img[y][x] == 0 and im_bw[y-i][x] == 1 and im_bw[y+i][x] == 1 and im_bw[y][x-i] == 1 and im_bw[y][x+i] == 1:
                            img[y][x] = 1
                r = 6
            except:
                r += 1
        i += 1
    return img
def median(output, quant, colors):
    im_bw = color(output, colors)
    img = im_bw.copy()
    if quant == 0:
        return img
    height, width = img.shape[:2]
    i = 1
    while i <= quant:
        r = 0
        while r <= 5:
            try:
                for x in range(0, width-r, 3):
                    for y in range(0, height-r, 3):
                        if x == width-1 or y == height-1:
                            img[y][x] = 0
                        n = 0
                        if img[y-i][x-i] == 1:
                            n += 1
                        if img[y-i][x] == 1:
                            n += 1
                        if img[y-i][x+i] == 1:
                            n += 1
                        if img[y][x-i] == 1:
                            n += 1
                        if img[y][x] == 1:
                            n += 1
                        if img[y][x+i] == 1:
                            n += 1
                        if img[y+i][x-i] == 1:
                            n += 1
                        if img[y+i][x] == 1:
                            n += 1
                        if img[y+i][x+i] == 1:
                            n += 1
                        if n >= 5:
                            img[y][x] = 1
                            img[y-i][x-i] = 1
                            img[y-i][x] = 1
                            img[y-i][x+i] = 1
                            img[y][x-i] = 1
                            img[y][x+i] = 1
                            img[y+i][x-i] = 1
                            img[y+i][x] = 1
                            img[y+i][x+i] = 1
                        else:
                            img[y][x] = 0
                            img[y-i][x-i] = 0
                            img[y-i][x] = 0
                            img[y-i][x+i] = 0
                            img[y][x-i] = 0
                            img[y][x+i] = 0
                            img[y+i][x-i] = 0
                            img[y+i][x] = 0
                            img[y+i][x+i] = 0
                r = 6
            except:
                r += 1
        i += 1
    return img