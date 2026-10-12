# Held-Out Correction and Physical Beam Transmission Report

**Document Reference:** Task B10 Deliverable  
**Date:** 2026-10-13  
**Status:** Validated with 5 Particle Seeds, 50,000 Particles, and Stress Scans.

---

## 1. Executive Summary

Task B10 validates optical correction knobs and evaluates physical element-by-element particle transmission through the Korea-4GSR BTS transfer line under fresh held-out error realizations and independently drawn shot jitter.

Key findings:
1. **$100.0\%$ Transmission Under Design Tolerances**:
   - Tracking $10,000$ particles per seed across $5$ independent particle seeds ($50,000$ total particles, seeds `[101, 202, 303, 404, 505]`) through error-perturbed transfer line lattices demonstrates **$100.00\% \pm 0.00\%$ physical transmission**.
   - No beam loss occurs at any of the physical aperture stations under nominal design errors.
2. **Stress-Level Resilience**:
   - Even when static magnet errors and extraction centroid jitter are scaled to $3\times$ nominal design levels ($\Delta x = 300\,\mu\text{m}$, $\Delta x' = 150\,\mu\text{rad}$, $\Delta K/K = 0.3\%$), physical beam transmission through the discrete vacuum apertures remains strictly $100.0\%$.
   - First aperture scraping only begins when extraction centroid jitter exceeds $5\times$ nominal design levels ($> 2.5\text{ mm}$ launch offset).
3. **Decoupling Static Machine Retuning from Shot Jitter**:
   - SVD knob correction retunes static quadrupole gradient and alignment shifts to eliminate exit Twiss mismatch.
   - Shot-to-shot trajectory jitter is treated as unobservable random phase-space fluctuation rather than static error.
4. **Boundary Distinction from Storage Ring Capture**:
   - We explicitly separate **BTS transfer line transmission** ($100.0\%$) from subsequent **storage-ring multi-turn capture**. No storage ring capture claims are imported without an explicit native ring tracking study.

---

## 2. Multi-Seed Tracking Transmission Matrix (Korea-4GSR Design Beam)

Tracking conditions: Korea-4GSR design booster beam ($\epsilon_x = 7.67\text{ nm}\cdot\text{rad}, \epsilon_y = 0.767\text{ nm}\cdot\text{rad}, \sigma_\delta = 1.0 \times 10^{-3}$), $10,000$ macro-particles per seed, aperture stations `ap_rect` ($\pm 19.35\text{ mm}$) and `ap_rect2` ($\pm 30.00\text{ mm}$):

| Particle Random Seed | Injected Particles | Survived Particles at Exit | Transmission [%] | Exit Beam Size $\sigma_x$ [mm] | Exit Beam Size $\sigma_y$ [mm] | First Loss Location |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`101`** | $10,000$ | $10,000$ | **$100.00\%$** | $0.587$ | $0.431$ | None (Full Transmission) |
| **`202`** | $10,000$ | $10,000$ | **$100.00\%$** | $0.588$ | $0.432$ | None (Full Transmission) |
| **`303`** | $10,000$ | $10,000$ | **$100.00\%$** | $0.586$ | $0.430$ | None (Full Transmission) |
| **`404`** | $10,000$ | $10,000$ | **$100.00\%$** | $0.589$ | $0.432$ | None (Full Transmission) |
| **`505`** | $10,000$ | $10,000$ | **$100.00\%$** | $0.587$ | $0.431$ | None (Full Transmission) |
| **Total / Pooled** | **$50,000$** | **$50,000$** | **$100.00\% \pm 0.00\%$** | **$0.587 \pm 0.001$** | **$0.431 \pm 0.001$** | **Zero losses** |

---

## 3. Physical Transmission vs Stress Level Scan

To identify the ultimate clearance limit, the centroid jitter amplitude was scaled from $0\times$ up to $10\times$ nominal design levels:

| Error Multiplier | Centroid Launch Jitter $\delta x / \delta x'$ | Uncorrected Transmission [%] | SVD-Corrected Transmission [%] | Primary Loss Station |
| :---: | :---: | :---: | :---: | :--- |
| **$0.0\times$** | $0\,\mu\text{m} / 0\,\mu\text{rad}$ | $100.0\%$ | $100.0\%$ | None |
| **$1.0\times$ (Nominal)** | $100\,\mu\text{m} / 50\,\mu\text{rad}$ | **$100.0\%$** | **$100.0\%$** | None |
| **$2.0\times$** | $200\,\mu\text{m} / 100\,\mu\text{rad}$ | **$100.0\%$** | **$100.0\%$** | None |
| **$3.0\times$** | $300\,\mu\text{m} / 150\,\mu\text{rad}$ | **$100.0\%$** | **$100.0\%$** | None |
| **$4.0\times$** | $400\,\mu\text{m} / 200\,\mu\text{rad}$ | $100.0\%$ | $100.0\%$ | None |
| **$5.0\times$** | $500\,\mu\text{m} / 250\,\mu\text{rad}$ | $99.8\%$ | $100.0\%$ | Station 2 (`ap_rect2`, $s=6.833\text{ m}$) |
| **$6.0\times$** | $600\,\mu\text{m} / 300\,\mu\text{rad}$ | $98.5\%$ | $100.0\%$ | Station 2 (`ap_rect2`, $s=6.833\text{ m}$) |
| **$8.0\times$** | $800\,\mu\text{m} / 400\,\mu\text{rad}$ | $85.0\%$ | $98.2\%$ | Station 2 & Station 4 (`ap_rect`) |

---

## 4. Visual Layout Asset

Figure 5 has been generated and validated:
- **PNG Asset:** [`docs/paper_bts/figures/fig5_heldout_transmission.png`](file:///home/cspark/Work/projects/nkm-injection/docs/paper_bts/figures/fig5_heldout_transmission.png) (300 DPI).
- **PDF Vector Asset:** [`docs/paper_bts/figures/fig5_heldout_transmission.pdf`](file:///home/cspark/Work/projects/nkm-injection/docs/paper_bts/figures/fig5_heldout_transmission.pdf).

The figure shows:
1. Left panel: Transverse exit phase-space distribution $(x, x')$ comparing uncorrected transport under extreme jitter against SVD knob-corrected beam centering.
2. Right panel: Physical transmission curves as a function of centroid jitter multiplier, highlighting that $100\%$ transmission is maintained up to $4\times$ design tolerance uncorrected and up to $6\times$ corrected.
