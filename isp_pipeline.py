from matplotlib import pyplot as plt
import numpy as np
import csv
import imageio
import time
from model.dpc import DPC
from model.blc import BLC
from model.aaf import AAF
from model.awb import WBGC
from model.cnf import CNF
from model.cfa import CFA
from model.gac import GC
from model.ccm import CCM
from model.csc import CSC
from model.bnf import BNF
from model.eeh import EE
from model.fcs import FCS
from model.bcc import BCC
from model.hsc import HSC
from model.nlm import NLM

raw_path = './raw/test.RAW'
config_path = './config/config.csv'
output_path_images = './output/images/'
output_path_bin = './output/binaries/'
output_path_bin_aaf = output_path_bin + 'rawimg_aaf.bin'
output_path_bin_awb = output_path_bin + 'rawimg_awb.bin'
output_path_bin_bcc = output_path_bin + 'yuvimg_bcc.bin'
output_path_bin_blc = output_path_bin + 'rawimg_blc.bin'
output_path_bin_bnf = output_path_bin + 'yuvimg_bnf.bin'
output_path_bin_ccm = output_path_bin + 'rgbimg_ccm.bin'
output_path_bin_cfa = output_path_bin + 'rgbimg_cfa.bin'
output_path_bin_cnf = output_path_bin + 'rawimg_cnf.bin'
output_path_bin_csc = output_path_bin + 'yuvimg_csc.bin'
output_path_bin_dpc = output_path_bin + 'rawimg_dpc.bin'
output_path_bin_ee = output_path_bin + 'yuvimg_ee.bin'
output_path_bin_fcs = output_path_bin + 'yuvimg_fcs.bin'
output_path_bin_gc = output_path_bin + 'rgbimg_gc.bin'
output_path_bin_hsc = output_path_bin + 'yuvimg_hsc.bin'
output_path_bin_nlm = output_path_bin + 'yuvimg_nlm.bin'

f = open(config_path, 'r', encoding='utf-8-sig')
with f:
    reader = csv.reader(f, delimiter=',')
    raw_h = 1280
    raw_w = 720
    dpc_thres = 30
    dpc_mode = 'gradient'
    dpc_clip = 1023
    bl_r = 0
    bl_gr = 0
    bl_gb = 0
    bl_b = 0
    alpha = 0
    beta = 0
    blc_clip = 1023
    bayer_pattern = 'rggb'
    r_gain = 1.5
    gr_gain = 1.0
    gb_gain = 1.0
    b_gain = 1.1
    awb_clip = 1023
    cfa_mode = 'malvar'
    cfa_clip = 1023
    ccm = np.zeros((3, 4))
    csc = np.zeros((3, 4))
    bnf_dw = np.zeros((5,5))
    bnf_rw = [1, 1, 1, 1]
    bnf_rthres = [32, 64, 128]
    bnf_clip = 255
    edge_filter = np.zeros((3, 5))
    ee_gain = [32, 128]
    ee_thres = [32, 64]
    ee_emclip = [-64, 64]
    fcs_edge = [32, 64]
    fcs_gain = 32
    fcs_intercept = 2
    fcs_slope = 3
    hue = 128
    saturation = 256
    hsc_clip = 255
    brightness = 10  # [-255, 255]
    contrast = 10 / pow(2, 5)  # [-32,128]
    bcc_clip = 255
    nlm_h = 10
    nlm_clip = 255
    for row in reader:
        parameter = row[0]
        value = row[1]
        description = row[2]
        print(parameter, value, description)
        if 'raw' in str(parameter):
            raw_w = int(value) if '_w' in str(parameter) else raw_w
            raw_h = int(value) if '_h' in str(parameter) else raw_h
        elif 'dpc' in str(parameter):
            dpc_thres = int(value) if '_thres' in str(parameter) else dpc_thres
            dpc_mode  = str(value) if '_mode' in str(parameter) else dpc_mode
            dpc_clip  = int(value) if '_clip' in str(parameter) else dpc_clip
        elif 'bl' in str(parameter):
            bl_r  = int(value) if '_r' in str(parameter) else bl_r
            bl_gr = int(value) if '_gr' in str(parameter) else bl_gr
            bl_gb = int(value) if '_gb' in str(parameter) else bl_gb
            bl_b  = int(value) if '_b' in str(parameter) else bl_b
            alpha = int(value) if '_alpha' in str(parameter) else alpha
            beta  = int(value) if '_beta' in str(parameter) else beta
            blc_clip = int(value) if '_clip' in str(parameter) else beta
        elif 'bayer_pattern' in str(parameter):
            bayer_pattern = str(value)
        elif 'awb' in str(parameter):
            r_gain  = int(value) if '_rgain' in str(parameter) else r_gain
            gr_gain = int(value) if '_grgain' in str(parameter) else gr_gain
            gb_gain = int(value) if '_gbgain' in str(parameter) else gb_gain
            b_gain  = int(value) if '_bgain' in str(parameter) else b_gain
            awb_clip = int(value) if '_clip' in str(parameter) else awb_clip
        elif 'cfa' in str(parameter):
            cfa_mode = str(value) if '_mode' in str(parameter) else cfa_mode
            cfa_clip = int(value) if '_clip' in str(parameter) else cfa_clip
        elif 'ccm' in str(parameter):
            ccm[0][0] = int(value) if '_00' in str(parameter) else ccm[0][0]
            ccm[0][1] = int(value) if '_01' in str(parameter) else ccm[0][1]
            ccm[0][2] = int(value) if '_02' in str(parameter) else ccm[0][2]
            ccm[0][3] = int(value) if '_03' in str(parameter) else ccm[0][3]
            ccm[1][0] = int(value) if '_10' in str(parameter) else ccm[1][0]
            ccm[1][1] = int(value) if '_11' in str(parameter) else ccm[1][1]
            ccm[1][2] = int(value) if '_12' in str(parameter) else ccm[1][2]
            ccm[1][3] = int(value) if '_13' in str(parameter) else ccm[1][3]
            ccm[2][0] = int(value) if '_20' in str(parameter) else ccm[2][0]
            ccm[2][1] = int(value) if '_21' in str(parameter) else ccm[2][1]
            ccm[2][2] = int(value) if '_22' in str(parameter) else ccm[2][2]
            ccm[2][3] = int(value) if '_23' in str(parameter) else ccm[2][3]
        elif 'csc' in str(parameter):
            csc[0][0] = 1024 * float(value) if '_00' in str(parameter) else csc[0][0]
            csc[0][1] = 1024 * float(value) if '_01' in str(parameter) else csc[0][1]
            csc[0][2] = 1024 * float(value) if '_02' in str(parameter) else csc[0][2]
            csc[0][3] = 1024 * float(value) if '_03' in str(parameter) else csc[0][3]
            csc[1][0] = 1024 * float(value) if '_10' in str(parameter) else csc[1][0]
            csc[1][1] = 1024 * float(value) if '_11' in str(parameter) else csc[1][1]
            csc[1][2] = 1024 * float(value) if '_12' in str(parameter) else csc[1][2]
            csc[1][3] = 1024 * float(value) if '_13' in str(parameter) else csc[1][3]
            csc[2][0] = 1024 * float(value) if '_20' in str(parameter) else csc[2][0]
            csc[2][1] = 1024 * float(value) if '_21' in str(parameter) else csc[2][1]
            csc[2][2] = 1024 * float(value) if '_22' in str(parameter) else csc[2][2]
            csc[2][3] = 1024 * float(value) if '_23' in str(parameter) else csc[2][3]
        elif 'bnf' in str(parameter):
            bnf_dw[0][0] = int(value) if '_dw_00' in str(parameter) else bnf_dw[0][0]
            bnf_dw[0][1] = int(value) if '_dw_01' in str(parameter) else bnf_dw[0][1]
            bnf_dw[0][2] = int(value) if '_dw_02' in str(parameter) else bnf_dw[0][2]
            bnf_dw[0][3] = int(value) if '_dw_03' in str(parameter) else bnf_dw[0][3]
            bnf_dw[0][4] = int(value) if '_dw_04' in str(parameter) else bnf_dw[0][4]
            bnf_dw[1][0] = int(value) if '_dw_10' in str(parameter) else bnf_dw[1][0]
            bnf_dw[1][1] = int(value) if '_dw_11' in str(parameter) else bnf_dw[1][1]
            bnf_dw[1][2] = int(value) if '_dw_12' in str(parameter) else bnf_dw[1][2]
            bnf_dw[1][3] = int(value) if '_dw_13' in str(parameter) else bnf_dw[1][3]
            bnf_dw[1][4] = int(value) if '_dw_14' in str(parameter) else bnf_dw[1][4]
            bnf_dw[2][0] = int(value) if '_dw_20' in str(parameter) else bnf_dw[2][0]
            bnf_dw[2][1] = int(value) if '_dw_21' in str(parameter) else bnf_dw[2][1]
            bnf_dw[2][2] = int(value) if '_dw_22' in str(parameter) else bnf_dw[2][2]
            bnf_dw[2][3] = int(value) if '_dw_23' in str(parameter) else bnf_dw[2][3]
            bnf_dw[2][4] = int(value) if '_dw_24' in str(parameter) else bnf_dw[2][4]
            bnf_rw[0] = int(value) if '_rw_0' in str(parameter) else bnf_rw[0]
            bnf_rw[1] = int(value) if '_rw_1' in str(parameter) else bnf_rw[1]
            bnf_rw[2] = int(value) if '_rw_2' in str(parameter) else bnf_rw[2]
            bnf_rw[3] = int(value) if '_rw_3' in str(parameter) else bnf_rw[3]
            bnf_rthres[0] = int(value) if '_rthres_0' in str(parameter) else bnf_rthres[0]
            bnf_rthres[1] = int(value) if '_rthres_1' in str(parameter) else bnf_rthres[1]
            bnf_rthres[2] = int(value) if '_rthres_2' in str(parameter) else bnf_rthres[2]
            bnf_clip = int(value) if '_clip' in str(parameter) else bnf_clip
        elif 'edge_filter' in str(parameter):
            edge_filter[0][0] = int(value) if '_00' in str(parameter) else edge_filter[0][0]
            edge_filter[0][1] = int(value) if '_01' in str(parameter) else edge_filter[0][1]
            edge_filter[0][2] = int(value) if '_02' in str(parameter) else edge_filter[0][2]
            edge_filter[0][3] = int(value) if '_03' in str(parameter) else edge_filter[0][3]
            edge_filter[0][4] = int(value) if '_04' in str(parameter) else edge_filter[0][4]
            edge_filter[1][0] = int(value) if '_10' in str(parameter) else edge_filter[1][0]
            edge_filter[1][1] = int(value) if '_11' in str(parameter) else edge_filter[1][1]
            edge_filter[1][2] = int(value) if '_12' in str(parameter) else edge_filter[1][2]
            edge_filter[1][3] = int(value) if '_13' in str(parameter) else edge_filter[1][3]
            edge_filter[1][4] = int(value) if '_14' in str(parameter) else edge_filter[1][4]
            edge_filter[2][0] = int(value) if '_20' in str(parameter) else edge_filter[2][0]
            edge_filter[2][1] = int(value) if '_21' in str(parameter) else edge_filter[2][1]
            edge_filter[2][2] = int(value) if '_22' in str(parameter) else edge_filter[2][2]
            edge_filter[2][3] = int(value) if '_23' in str(parameter) else edge_filter[2][3]
            edge_filter[2][4] = int(value) if '_24' in str(parameter) else edge_filter[2][4]
        elif 'ee' in str(parameter):
            ee_gain[0] = int(value) if 'gain_min' in str(parameter) else ee_gain[0]
            ee_gain[1] = int(value) if 'gain_max' in str(parameter) else ee_gain[1]
            ee_thres[0] = int(value) if 'thres_min' in str(parameter) else ee_thres[0]
            ee_thres[1] = int(value) if 'thres_max' in str(parameter) else ee_thres[1]
            ee_emclip[0] = int(value) if 'emclip_min' in str(parameter) else ee_emclip[0]
            ee_emclip[1] = int(value) if 'emclip_max' in str(parameter) else ee_emclip[1]
        elif 'fcs' in str(parameter):
            fcs_edge[0] = int(value) if 'edge_min' in str(parameter) else fcs_edge[0]
            fcs_edge[1] = int(value) if 'edge_min' in str(parameter) else fcs_edge[1]
            fcs_gain = int(value) if '_gain' in str(parameter) else fcs_gain
            fcs_intercept = int(value) if '_intercept' in str(parameter) else fcs_intercept
            fcs_slope = int(value) if '_slope' in str(parameter) else fcs_slope
        elif 'nlm' in str(parameter):
            nlm_h = int(value) if '_h' in str(parameter) else nlm_h
            nlm_clip = int(value) if '_clip' in str(parameter) else nlm_clip
        else:
            hue = int(value) if 'hue' in str(parameter) else hue
            saturation = int(value) if 'saturation' in str(parameter) else saturation
            hsc_clip = int(value) if 'hsc_clip' in str(parameter) else hsc_clip
            brightness = int(value) if 'brightness' in str(parameter) else brightness
            contrast = int(value) if 'contrast' in str(parameter) else contrast
            bcc_clip = int(value) if 'bcc_clip' in str(parameter) else bcc_clip

total_start_time = time.perf_counter()
step_start_time = time.perf_counter()
step = 1

rawimg = np.fromfile(raw_path, dtype='uint16', sep='')
rawimg = rawimg.reshape([raw_h, raw_w])
print(50*'-' + '\nLoading RAW Image Done......')

step_end_time = time.perf_counter()
step_time = (step_end_time - step_start_time) * 1000
total_time = (step_end_time - total_start_time) * 1000
print(f"Step {step} Time: {step_time:.3f} milliseconds (Total: {total_time:.3f} milliseconds)")
step_start_time = time.perf_counter()
#plt.imshow(rawimg, cmap='gray')
#plt.show()

# 1. dead pixel correction
dpc = DPC(rawimg, dpc_thres, dpc_mode, dpc_clip)
rawimg_dpc = dpc.execute()
print(50*'-' + '\nDead Pixel Correction Done......')

rawimg_dpc.astype('uint16').tofile(output_path_images + f'step_{step}.dng')
rawimg_dpc.astype(np.uint16).tofile(output_path_bin + 'rawimg_dpc.bin')
step_end_time = time.perf_counter()
step_time = (step_end_time - step_start_time) * 1000
total_time = (step_end_time - total_start_time) * 1000
print(f"Step {step} Time: {step_time:.3f} milliseconds (Total: {total_time:.3f} milliseconds)")
step_start_time = time.perf_counter()
step += 1


#plt.imshow(rawimg_dpc, cmap='gray')
#plt.show()

# 2. black level compensation
rawimg_dpc = np.fromfile(output_path_bin_dpc, dtype=np.uint16, sep='')
rawimg_dpc = rawimg_dpc.reshape([raw_h, raw_w])
parameter = [bl_r, bl_gr, bl_gb, bl_b, alpha, beta]
blc = BLC(rawimg_dpc, parameter, bayer_pattern, blc_clip)
rawimg_blc = blc.execute()
print(50*'-' + '\nBlack Level Compensation Done......')

rawimg_blc.astype('uint16').tofile(output_path_images + f'step_{step}.dng')
rawimg_blc.astype(np.uint16).tofile(output_path_bin + 'rawimg_blc.bin')
step_end_time = time.perf_counter()
step_time = (step_end_time - step_start_time) * 1000
total_time = (step_end_time - total_start_time) * 1000
print(f"Step {step} Time: {step_time:.3f} milliseconds (Total: {total_time:.3f} milliseconds)")
step_start_time = time.perf_counter()
step += 1


#plt.imshow(rawimg_blc, cmap='gray')
#plt.show()

# lens shading correction

# 3. anti-aliasing filter
rawimg_blc = np.fromfile(output_path_bin_blc, dtype=np.uint16, sep='')
rawimg_blc = rawimg_blc.reshape([raw_h, raw_w])
aaf = AAF(rawimg_blc)
rawimg_aaf = aaf.execute()
print(50*'-' + '\nAnti-aliasing Filtering Done......')

rawimg_aaf.astype('uint16').tofile(output_path_images + f'step_{step}.dng')
rawimg_aaf.tofile(output_path_bin + 'rawimg_aaf.bin')
rawimg_aaf.astype(np.uint16).tofile(output_path_bin + 'rawimg_aaf.bin')
step_end_time = time.perf_counter()
step_time = (step_end_time - step_start_time) * 1000
total_time = (step_end_time - total_start_time) * 1000
print(f"Step {step} Time: {step_time:.3f} milliseconds (Total: {total_time:.3f} milliseconds)")
step_start_time = time.perf_counter()
step += 1


#plt.imshow(rawimg_aaf, cmap='gray')
#plt.show()

#rawimg_diff = rawimg_blc - rawimg_aaf
#plt.imshow(rawimg_diff, cmap='gray')
#plt.show()

# 4. white balance gain control
rawimg_aaf = np.fromfile(output_path_bin_aaf, dtype=np.uint16, sep='')
rawimg_aaf = rawimg_aaf.reshape([raw_h, raw_w])
parameter = [r_gain, gr_gain, gb_gain, b_gain]
awb = WBGC(rawimg_aaf, parameter, bayer_pattern, awb_clip)
rawimg_awb = awb.execute()
print(50*'-' + '\nWhite Balance Gain Done......')

rawimg_awb.astype('uint16').tofile(output_path_images + f'step_{step}.dng')
rawimg_awb.astype(np.uint16).tofile(output_path_bin + 'rawimg_awb.bin')
step_end_time = time.perf_counter()
step_time = (step_end_time - step_start_time) * 1000
total_time = (step_end_time - total_start_time) * 1000
print(f"Step {step} Time: {step_time:.3f} milliseconds (Total: {total_time:.3f} milliseconds)")
step_start_time = time.perf_counter()
step += 1


#plt.imshow(rawimg_awb, cmap='gray')
#plt.show()

# 5. chroma noise filtering
rawimg_awb = np.fromfile(output_path_bin_awb, dtype=np.uint16, sep='')
rawimg_awb = rawimg_awb.reshape([raw_h, raw_w])
cnf = CNF(rawimg_awb, bayer_pattern, 0, parameter, 1023)
rawimg_cnf = cnf.execute()
print(50*'-' + '\nChroma Noise Filtering Done......')

rawimg_cnf.astype('uint16').tofile(output_path_images + f'step_{step}.dng')
rawimg_cnf.astype(np.uint16).tofile(output_path_bin + 'rawimg_cnf.bin')
step_end_time = time.perf_counter()
step_time = (step_end_time - step_start_time) * 1000
total_time = (step_end_time - total_start_time) * 1000
print(f"Step {step} Time: {step_time:.3f} milliseconds (Total: {total_time:.3f} milliseconds)")
step_start_time = time.perf_counter()
step += 1


#plt.imshow(rawimg_cnf/4, cmap='gray')
#plt.show()

# 6. color filter array interpolation
rawimg_cnf = np.fromfile(output_path_bin_cnf, dtype=np.uint16, sep='')
rawimg_cnf = rawimg_cnf.reshape([raw_h, raw_w])
cfa = CFA(rawimg_cnf, cfa_mode, bayer_pattern, cfa_clip)
rgbimg_cfa = cfa.execute()
print(50*'-' + '\nDemosaicing Done......')

rgbimg_cfa_uint8 = (rgbimg_cfa).astype(np.uint8)
imageio.imwrite(output_path_images + f'step_{step}.tiff', rgbimg_cfa_uint8)

rgbimg_cfa_normalized = rgbimg_cfa / np.max(rgbimg_cfa)
rgbimg_cfa_scaled = (rgbimg_cfa_normalized * 255).astype(np.uint8)
imageio.imwrite(output_path_images + f'step_{step}_normalised.tiff', rgbimg_cfa_scaled)
rgbimg_cfa.tofile(output_path_bin + 'rgbimg_cfa.bin')
step_end_time = time.perf_counter()
step_time = (step_end_time - step_start_time) * 1000
total_time = (step_end_time - total_start_time) * 1000
print(f"Step {step} Time: {step_time:.3f} milliseconds (Total: {total_time:.3f} milliseconds)")
step_start_time = time.perf_counter()
step += 1


#plt.imshow(rgbimg_cfa/4)
#plt.show()

# 7. color correction matrix
ccm = CCM(rgbimg_cfa, ccm)
rgbimg_ccm = ccm.execute()
print(50*'-' + '\nColor Correction Done......')

rgbimg_ccm_uint8 = (rgbimg_ccm).astype(np.uint8)
imageio.imwrite(output_path_images + f'step_{step}.tiff', rgbimg_ccm_uint8)

rgbimg_ccm_normalized = rgbimg_ccm / np.max(rgbimg_ccm)
rgbimg_ccm_scaled = (rgbimg_ccm_normalized * 255).astype(np.uint8)
imageio.imwrite(output_path_images + f'step_{step}_normalised.tiff', rgbimg_ccm_scaled)
rgbimg_ccm.tofile(output_path_bin + 'rgbimg_ccm.bin')
step_end_time = time.perf_counter()
step_time = (step_end_time - step_start_time) * 1000
total_time = (step_end_time - total_start_time) * 1000
print(f"Step {step} Time: {step_time:.3f} milliseconds (Total: {total_time:.3f} milliseconds)")
step_start_time = time.perf_counter()
step += 1


#plt.imshow(rgbimg_ccm)
#plt.show()

# 8. gamma correction
# look up table
bw = 10
gamma = 0.5
mode = 'rgb'

maxval = pow(2,bw)
ind = range(0, maxval)
val = [round(pow(float(i)/maxval, gamma) * maxval) for i in ind]
lut = dict(zip(ind, val))
#print(ind, val, lut)
gc = GC(rgbimg_ccm, lut, mode)
rgbimg_gc = gc.execute()
print(50*'-' + '\nGamma Correction Done......')

rgbimg_gc_uint8 = (rgbimg_gc).astype(np.uint8)
imageio.imwrite(output_path_images + f'step_{step}.tiff', rgbimg_gc_uint8)
rgbimg_gc_normalized = rgbimg_gc / np.max(rgbimg_gc)
rgbimg_gc_scaled = (rgbimg_gc_normalized * 255).astype(np.uint8)
imageio.imwrite(output_path_images + f'step_{step}_normalised.tiff', rgbimg_gc_scaled)
rgbimg_gc.tofile(output_path_bin + 'rgbimg_gc.bin')
step_end_time = time.perf_counter()
step_time = (step_end_time - step_start_time) * 1000
total_time = (step_end_time - total_start_time) * 1000
print(f"Step {step} Time: {step_time:.3f} milliseconds (Total: {total_time:.3f} milliseconds)")
step_start_time = time.perf_counter()
step += 1


#plt.imshow(rgbimg_gc)
#plt.show()

# 9. color space conversion
csc = CSC(rgbimg_ccm, csc)
yuvimg_csc = csc.execute()
print(50*'-' + '\nColor Space Conversion Done......')

yuvimg_csc_uint8 = (yuvimg_csc).astype(np.uint8)
imageio.imwrite(output_path_images + f'step_{step}.tiff', yuvimg_csc_uint8)

yuvimg_csc_normalized = yuvimg_csc / np.max(yuvimg_csc)
yuvimg_csc_scaled = (yuvimg_csc_normalized * 255).astype(np.uint8)
imageio.imwrite(output_path_images + f'step_{step}_normalised.tiff', yuvimg_csc_scaled)
yuvimg_csc.tofile(output_path_bin + 'yuvimg_csc.bin')
step_end_time = time.perf_counter()
step_time = (step_end_time - step_start_time) * 1000
total_time = (step_end_time - total_start_time) * 1000
print(f"Step {step} Time: {step_time:.3f} milliseconds (Total: {total_time:.3f} milliseconds)")
step_start_time = time.perf_counter()
step += 1


#plt.imshow(yuvimg_csc[:,:,0], cmap='gray')
#plt.show()

# 10. non-local means denoising
nlm = NLM(yuvimg_csc[:,:,0], 1, 4, nlm_h, nlm_clip)
yuvimg_nlm = nlm.execute()
print(50*'-' + '\nNon Local Means Denoising Done......')

yuvimg_nlm.astype('uint16').tofile(output_path_images + f'step_{step}.dng')
yuvimg_nlm.tofile(output_path_bin + 'yuvimg_nlm.bin')
step_end_time = time.perf_counter()
step_time = (step_end_time - step_start_time) * 1000
total_time = (step_end_time - total_start_time) * 1000
print(f"Step {step} Time: {step_time:.3f} milliseconds (Total: {total_time:.3f} milliseconds)")
step_start_time = time.perf_counter()
step += 1


#plt.imshow(yuvimg_nlm, cmap='gray')
#plt.show()

# 11. bilateral filter
bnf = BNF(yuvimg_nlm, bnf_dw, bnf_rw, bnf_rthres, bnf_clip)
yuvimg_bnf = bnf.execute()
print(50*'-' + '\nBilateral Filtering Done......')

yuvimg_bnf.astype('uint16').tofile(output_path_images + f'step_{step}.dng')
yuvimg_bnf.tofile(output_path_bin + 'yuvimg_bnf.bin')
step_end_time = time.perf_counter()
step_time = (step_end_time - step_start_time) * 1000
total_time = (step_end_time - total_start_time) * 1000
print(f"Step {step} Time: {step_time:.3f} milliseconds (Total: {total_time:.3f} milliseconds)")
step_start_time = time.perf_counter()
step += 1


#plt.imshow(yuvimg_bnf, cmap='gray')
#plt.show()

# 12. edge enhancement
ee = EE(yuvimg_bnf[:,:], edge_filter, ee_gain, ee_thres, ee_emclip)
yuvimg_ee, yuvimg_edgemap = ee.execute()
print(50*'-' + '\nEdge Enhancement Done......')

yuvimg_bnf.astype('uint16').tofile(output_path_images + f'step_{step}.dng')
yuvimg_ee.tofile(output_path_bin + 'yuvimg_ee.bin')
step_end_time = time.perf_counter()
step_time = (step_end_time - step_start_time) * 1000
total_time = (step_end_time - total_start_time) * 1000
print(f"Step {step} Time: {step_time:.3f} milliseconds (Total: {total_time:.3f} milliseconds)")
step_start_time = time.perf_counter()
step += 1


#plt.imshow(yuvimg_ee)
#plt.show()
#plt.imshow(yuvimg_edgemap)
#plt.show()

# 13. false color suppresion
fcs = FCS(yuvimg_csc[:,:,1:3], yuvimg_edgemap, fcs_edge, fcs_gain, fcs_intercept, fcs_slope)
yuvimg_fcs = fcs.execute()
print(50*'-' + '\nFalse Color Suppresion Done......')

yuvimg_fcs_uint8 = (yuvimg_fcs).astype(np.uint8)
imageio.imwrite(output_path_images + f'step_{step}.tiff', yuvimg_fcs_uint8)

yuvimg_fcs_normalized = yuvimg_fcs / np.max(yuvimg_fcs)
yuvimg_fcs_scaled = (yuvimg_fcs_normalized * 255).astype(np.uint8)
imageio.imwrite(output_path_images + f'step_{step}_normalised.tiff', yuvimg_fcs_scaled)
yuvimg_fcs.tofile(output_path_bin + 'yuvimg_fcs.bin')
step_end_time = time.perf_counter()
step_time = (step_end_time - step_start_time) * 1000
total_time = (step_end_time - total_start_time) * 1000
print(f"Step {step} Time: {step_time:.3f} milliseconds (Total: {total_time:.3f} milliseconds)")
step_start_time = time.perf_counter()
step += 1


#plt.imshow(yuvimg_fcs)
#plt.show()

# 14. hue/saturation control
hsc = HSC(yuvimg_fcs, hue, saturation, hsc_clip)
yuvimg_hsc = hsc.execute()
print(50*'-' + '\nHue/Saturation Adjustment Done......')

yuvimg_hsc_uint8 = (yuvimg_hsc).astype(np.uint8)
imageio.imwrite(output_path_images + f'step_{step}.tiff', yuvimg_hsc_uint8)
yuvimg_hsc_normalized = yuvimg_hsc / np.max(yuvimg_hsc)
yuvimg_hsc_scaled = (yuvimg_hsc_normalized * 255).astype(np.uint8)
imageio.imwrite(output_path_images + f'step_{step}_normalised.tiff', yuvimg_hsc_scaled)
yuvimg_hsc.tofile(output_path_bin + 'yuvimg_hsc.bin')
step_end_time = time.perf_counter()
step_time = (step_end_time - step_start_time) * 1000
total_time = (step_end_time - total_start_time) * 1000
print(f"Step {step} Time: {step_time:.3f} milliseconds (Total: {total_time:.3f} milliseconds)")
step_start_time = time.perf_counter()
step += 1


#plt.imshow(yuvimg_hsc)
#plt.show()

# 15. brightness/contrast control
contrast = contrast / pow(2,5)    #[-32,128]
bcc = BCC(yuvimg_ee, brightness, contrast, bcc_clip)
yuvimg_bcc = bcc.execute()
print(50*'-' + '\nBrightness/Contrast Adjustment Done......')

yuvimg_bcc.astype('uint16').tofile(output_path_images + f'step_{step}.dng')
yuvimg_bcc.tofile(output_path_bin + 'yuvimg_bcc.bin')
step_end_time = time.perf_counter()
step_time = (step_end_time - step_start_time) * 1000
total_time = (step_end_time - total_start_time) * 1000
print(f"Step {step} Time: {step_time:.3f} milliseconds (Total: {total_time:.3f} milliseconds)")
step_start_time = time.perf_counter()
step += 1


#plt.imshow(yuvimg_bcc)
#plt.show()

yuvimg_out = np.empty((raw_h, raw_w, 3), dtype=np.uint8)
yuvimg_out[:,:,0] = yuvimg_bcc
yuvimg_out[:,:,1:3] = yuvimg_hsc

total_end_time = time.perf_counter()
total_time = (total_end_time - total_start_time) * 1000
print(f"Total Time: {total_time:.3f} milliseconds")

plt.imshow(yuvimg_out)
plt.show()

yuvimg_out_uint8 = (yuvimg_out).astype(np.uint8)
yuvimg_out_uint8.tofile(output_path_images + f'final.raw')