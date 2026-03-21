#!/usr/bin/env python3
"""
OPTIMIZATIONLOCK CONFIGURATOR v1.4.3
A Designer's Republic-inspired GUI for editing Deadlock's gameinfo.gi & video.txt
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font as tkfont
import os
import re
import shutil
import sys

# Fix blurry UI on Windows high-DPI displays — MUST run before tkinter init
if sys.platform == "win32":
    try:
        import ctypes
        # Per-Monitor V2 DPI awareness (best for Win10 1703+)
        awareness = ctypes.c_int()
        ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))
        if awareness.value == 0:  # only set if not already set
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

# ─── CONVAR DEFINITIONS (gameinfo.gi) ─────────────────────────────────────────
# (cvar_name, config_value, default_value, description, category, value_type, options/range)

CONVARS = [
    # ═══ OUTLINES ═══
    ("citadel_trooper_glow_disabled", "0", "0", "Disable friendly/enemy minion glow", "OUTLINES", "bool", None),
    ("citadel_boss_glow_disabled", "1", "0", "Disable boss and walker glow/highlight", "OUTLINES", "bool", None),
    ("citadel_player_glow_disabled", "0", "0", "Disable player glow/highlight when pinged", "OUTLINES", "bool", None),
    ("r_citadel_npr_outlines_max_dist", "1000", "1000", "Outline max render distance", "OUTLINES", "int", (0, 5000)),
    # ═══ FOV ═══
    ("citadel_camera_hero_fov", "110", "90", "Camera FOV when following hero", "FOV", "int", (70, 130)),
    # ═══ HUD ═══
    ("citadel_unit_status_use_new", "1", "0", "Use new health bar style", "HUD", "bool", None),
    ("citadel_hud_objective_health_enabled", "2", "2", "Obj health: 0=Off 1=Shrines 2=T1/T2 3=Barracks", "HUD", "choice", ["0", "1", "2", "3"]),
    ("citadel_damage_report_enable", "1", "1", "Enable incoming/outgoing damage tab", "HUD", "bool", None),
    ("citadel_hideout_ball_show_juggle_count", "1", "0", "Show hideout ball juggle counter", "HUD", "bool", None),
    ("citadel_hideout_ball_show_juggle_fx", "1", "0", "Show juggle visual FX", "HUD", "bool", None),
    ("citadel_crosshair_hit_marker_duration", "-0.001", "0.1", "Hitmarker duration (-0.001 to remove)", "HUD", "float", (-0.001, 1.0)),
    # ═══ LIGHTING ═══
    ("lb_enable_stationary_lights", "1", "1", "Stationary lights (flatter but faster if off)", "LIGHTING", "bool", None),
    ("lb_enable_dynamic_lights", "0", "1", "Dynamic lights (walker, shop, abilities)", "LIGHTING", "bool", None),
    ("lb_enable_baked_shadows", "1", "1", "Baked shadows", "LIGHTING", "bool", None),
    # ═══ SKYBOX ═══
    ("r_drawskybox", "1", "1", "Draw 2D skybox", "SKYBOX", "bool", None),
    ("r_draw3dskybox", "0", "1", "Draw 3D skybox layer", "SKYBOX", "bool", None),
    # ═══ FPS ═══
    ("fps_max", "0", "400", "Max FPS in-game (0=unlimited)", "FPS", "int", (0, 999)),
    ("engine_no_focus_sleep", "20", "20", "Sleep ms when unfocused", "FPS", "int", (0, 100)),
    ("engine_low_latency_sleep_after_client_tick", "1", "0", "Low-latency sleep after client tick", "FPS", "bool", None),
    ("panorama_max_fps", "15", "120", "Menu/UI FPS cap", "FPS", "int", (0, 240)),
    ("panorama_max_overlay_fps", "15", "60", "Overlay FPS cap", "FPS", "int", (0, 240)),
    # ═══ CULLING ═══
    ("r_size_cull_threshold", "0.7", "0.8", "Small object cull threshold (higher=more culling)", "CULLING", "float", (0.0, 2.0)),
    # ═══ CAMERA ═══
    ("r_citadel_clip_sphere_min_opacity", "0", "40", "Pinhole camera blur (0=off)", "CAMERA", "int", (0, 100)),
    # ═══ UI ═══
    ("r_citadel_enable_pano_world_blur", "false", "true", "Panorama world blur", "UI", "bool_str", None),
    ("r_dashboard_render_quality", "0", "1", "Dashboard render quality", "UI", "choice", ["0", "1"]),
    ("panorama_disable_box_shadow", "1", "0", "Disable UI box shadows", "UI", "bool", None),
    ("panorama_disable_blur", "1", "0", "Disable UI blur effects", "UI", "bool", None),
    ("panorama_allow_transitions", "false", "1", "UI animations (shop etc)", "UI", "bool_str", None),
    ("closecaption", "false", "true", "Closed captions", "UI", "bool_str", None),
    # ═══ SHADOWS ═══
    ("r_shadows", "0", "1", "Dynamic shadows", "SHADOWS", "bool", None),
    ("r_citadel_shadow_quality", "0", "2", "Shadow quality level", "SHADOWS", "choice", ["0", "1", "2", "3"]),
    ("r_citadel_gpu_culling_shadows", "1", "0", "GPU-driven shadow culling", "SHADOWS", "bool", None),
    ("csm_max_shadow_dist_override", "0", "1024", "CSM max distance override", "SHADOWS", "int", (0, 4096)),
    ("r_size_cull_threshold_shadow", "1", "0.2", "Shadow size cull threshold", "SHADOWS", "float", (0.0, 2.0)),
    ("lb_enable_shadow_casting", "0", "1", "Light shadow casting", "SHADOWS", "bool", None),
    ("lb_barnlight_shadowmap_scale", "0.5", "1", "Barnlight shadowmap scale", "SHADOWS", "float", (0.0, 2.0)),
    ("lb_csm_cascade_size_override", "1", "1536", "CSM cascade size override", "SHADOWS", "int", (0, 4096)),
    ("lb_csm_override_staticgeo_cascades", "0", "1", "Static geometry cascades", "SHADOWS", "bool", None),
    ("lb_sun_csm_size_cull_threshold_texels", "30", "10", "CSM texel cull threshold", "SHADOWS", "int", (0, 100)),
    ("lb_dynamic_shadow_resolution_base", "256", "1536", "Dynamic shadow resolution", "SHADOWS", "int", (64, 4096)),
    ("sc_disable_spotlight_shadows", "1", "0", "Disable spotlight shadows", "SHADOWS", "bool", None),
    ("cl_globallight_shadow_mode", "0", "2", "Global light shadow mode", "SHADOWS", "choice", ["0", "1", "2"]),
    # ═══ DEEP LIGHTING ═══
    ("r_directlighting", "false", "true", "Direct lighting", "DEEP LIGHTING", "bool_str", None),
    ("r_rendersun", "0", "1", "Sun lighting", "DEEP LIGHTING", "bool", None),
    ("cl_retire_low_priority_lights", "1", "0", "Retire low-priority lights", "DEEP LIGHTING", "bool", None),
    ("r_lightmap_size", "4", "65536", "Max lightmap resolution", "DEEP LIGHTING", "int", (4, 65536)),
    ("r_lightmap_size_directional_irradiance", "4", "-1", "Directional irradiance lightmap size", "DEEP LIGHTING", "int", (-1, 65536)),
    ("r_ssao", "0", "1", "Screen-space ambient occlusion", "DEEP LIGHTING", "bool", None),
    ("r_ssao_strength", "0", "1.2", "SSAO strength", "DEEP LIGHTING", "float", (0.0, 3.0)),
    ("r_citadel_ssao_quality", "0", "3", "SSAO quality level", "DEEP LIGHTING", "choice", ["0", "1", "2", "3"]),
    ("mat_set_shader_quality", "0", "null", "Shader quality (0 or 1)", "DEEP LIGHTING", "choice", ["0", "1"]),
    ("r_distancefield_enable", "0", "1", "Distance field system", "DEEP LIGHTING", "bool", None),
    ("r_citadel_distancefield_farfield_enable", "0", "1", "Far-field distance field", "DEEP LIGHTING", "bool", None),
    # ═══ MODELS ═══
    ("skeleton_instance_lod_optimization", "1", "0", "Skeleton LOD optimization", "MODELS", "bool", None),
    ("enable_boneflex", "0", "1", "Bone flex (facial/mesh flex)", "MODELS", "bool", None),
    ("r_hair_ao", "0", "1", "Hair ambient occlusion", "MODELS", "bool", None),
    ("ik_final_fixup_enable", "0", "1", "Final IK fixup pass", "MODELS", "bool", None),
    ("cloth_sim_on_tick", "0", "1", "Cloth sim every tick", "MODELS", "bool", None),
    # ═══ VISUAL ═══
    ("mat_colorcorrection", "1", "1", "Color correction", "VISUAL", "bool", None),
    ("r_drawdecals", "1", "1", "Render decals", "VISUAL", "bool", None),
    ("r_depth_of_field", "0", "1", "Depth of field", "VISUAL", "bool", None),
    ("r_effects_bloom", "0", "1", "Effects bloom", "VISUAL", "bool", None),
    ("r_post_bloom", "0", "1", "Post-process bloom", "VISUAL", "bool", None),
    ("r_enable_volume_fog", "0", "1", "Volumetric fog", "VISUAL", "bool", None),
    ("r_enable_gradient_fog", "0", "1", "Gradient fog", "VISUAL", "bool", None),
    ("r_enable_cubemap_fog", "0", "1", "Cubemap fog", "VISUAL", "bool", None),
    ("r_citadel_fog_quality", "0", "1", "Fog quality level", "VISUAL", "choice", ["0", "1", "2"]),
    ("cl_show_splashes", "0", "1", "Splash effects", "VISUAL", "bool", None),
    ("violence_hblood", "0", "1", "Human blood effects", "VISUAL", "bool", None),
    ("violence_ablood", "0", "1", "Alien blood effects", "VISUAL", "bool", None),
    ("sc_clutter_enable", "0", "1", "Clutter props (debris)", "VISUAL", "bool", None),
    # ═══ SYSTEM ═══
    ("gpu_level", "1", "3", "GPU level", "SYSTEM", "choice", ["0", "1", "2", "3"]),
    ("gpu_mem_level", "1", "2", "GPU memory level", "SYSTEM", "choice", ["0", "1", "2"]),
    ("cpu_level", "1", "2", "CPU level", "SYSTEM", "choice", ["0", "1", "2"]),
    # ═══ PARTICLES ═══
    ("r_particle_max_detail_level", "0", "3", "Particle max detail level", "PARTICLES", "choice", ["0", "1", "2", "3"]),
    ("particle_cluster_nodraw", "1", "0", "Skip drawing particle clusters", "PARTICLES", "bool", None),
    ("r_RainParticleDensity", "0", "1", "Rain particle density", "PARTICLES", "float", (0.0, 1.0)),
    ("r_world_wind_strength", "0", "40", "Wind effects strength", "PARTICLES", "int", (0, 100)),
    ("cl_particle_fallback_multiplier", "4", "0", "Particle fallback aggression", "PARTICLES", "int", (0, 10)),
    # ═══ LOD ═══
    ("sc_screen_size_lod_scale_override", "0.56", "-1", "LOD scale (-1=default, lower=less polys)", "LOD", "float", (-1.0, 2.0)),
    ("sc_instanced_mesh_lod_bias", "15", "1.25", "Instanced mesh LOD bias", "LOD", "float", (0.0, 30.0)),
    ("sc_fade_distance_scale_override", "180", "-1", "Object fade distance", "LOD", "int", (-1, 500)),
    ("sv_pvs_max_distance", "2800", "0", "Max player render distance", "LOD", "int", (0, 10000)),
    ("mat_viewportscale", "0.01", "1", "Viewport LOD scale", "LOD", "float", (0.01, 1.0)),
    ("r_mapextents", "4500", "16384", "Far clipping plane", "LOD", "int", (1000, 32000)),
    # ═══ ROPES ═══
    ("r_drawropes", "0", "1", "Draw ropes", "ROPES", "bool", None),
    ("rope_collide", "0", "1", "Rope collision simulation", "ROPES", "bool", None),
    ("rope_subdiv", "0", "2", "Rope subdivision quality", "ROPES", "int", (0, 8)),
    # ═══ RAGDOLLS ═══
    ("cl_disable_ragdolls", "0", "0", "Disable ragdolls (can break Doorman ult)", "RAGDOLLS", "bool", None),
    ("ragdoll_parallel_pose_control", "1", "0", "Multithreaded ragdoll handling", "RAGDOLLS", "bool", None),
    # ═══ GRASS ═══
    ("r_grass_quality", "0", "2", "Grass quality", "GRASS", "choice", ["0", "1", "2"]),
    ("r_grass_start_fade", "0", "0", "Grass close fade distance", "GRASS", "int", (0, 500)),
    ("r_grass_end_fade", "0", "300", "Grass far fade distance", "GRASS", "int", (0, 1000)),
]

GAMEINFO_CATEGORIES = [
    "FOV", "OUTLINES", "HUD", "LIGHTING", "SKYBOX", "FPS",
    "SHADOWS", "DEEP LIGHTING", "UI", "VISUAL", "MODELS",
    "PARTICLES", "CULLING", "LOD", "ROPES", "RAGDOLLS", "GRASS",
    "SYSTEM", "CAMERA",
]

# ─── VIDEO.TXT DEFINITIONS ───────────────────────────────────────────────────
# (key, recommended_value, description, category, value_type, options/range)

VIDEO_SETTINGS = [
    # ═══ DEVICE ═══
    ("VendorID", "", "GPU vendor: NVIDIA=4318 AMD=4098 Intel=32902", "VID: DEVICE", "string", None),
    ("DeviceID", "", "Your GPU model ID (read from your original video.txt)", "VID: DEVICE", "string", None),
    # ═══ DISPLAY ═══
    ("setting.defaultres", "1920", "Monitor width", "VID: DISPLAY", "string", None),
    ("setting.defaultresheight", "1080", "Monitor height", "VID: DISPLAY", "string", None),
    ("setting.recommendedheight", "1080", "Same as defaultresheight", "VID: DISPLAY", "string", None),
    ("setting.refreshrate_numerator", "144", "Monitor refresh rate (Hz)", "VID: DISPLAY", "string", None),
    ("setting.refreshrate_denominator", "1", "Refresh rate denominator (leave at 1)", "VID: DISPLAY", "string", None),
    ("setting.fullscreen", "1", "1=Exclusive Fullscreen 0=Borderless", "VID: DISPLAY", "choice", ["0", "1"]),
    ("setting.nowindowborder", "1", "Borderless window", "VID: DISPLAY", "choice", ["0", "1"]),
    ("setting.monitor_index", "0", "0=Primary 1=Second monitor", "VID: DISPLAY", "choice", ["0", "1", "2"]),
    ("setting.fullscreen_min_on_focus_loss", "1", "Minimize on focus loss", "VID: DISPLAY", "choice", ["0", "1"]),
    ("setting.high_dpi", "0", "High DPI mode", "VID: DISPLAY", "choice", ["0", "1"]),
    ("setting.aspectratiomode", "0", "Aspect ratio mode", "VID: DISPLAY", "choice", ["0", "1", "2"]),
    ("setting.r_fullscreen_gamma", "2.100000", "Fullscreen gamma", "VID: DISPLAY", "string", None),
    # ═══ PERFORMANCE ═══
    ("setting.cpu_level", "1", "CPU quality level", "VID: PERFORMANCE", "choice", ["0", "1", "2", "3"]),
    ("setting.gpu_level", "1", "GPU quality level", "VID: PERFORMANCE", "choice", ["0", "1", "2", "3"]),
    ("setting.mem_level", "3", "RAM: 4-8GB=1 12-16GB=2 24GB+=3", "VID: PERFORMANCE", "choice", ["1", "2", "3"]),
    ("setting.gpu_mem_level", "3", "VRAM: 2-4GB=1 6-8GB=2 12GB+=3", "VID: PERFORMANCE", "choice", ["1", "2", "3"]),
    ("setting.fps_max", "0", "FPS cap (0=uncapped)", "VID: PERFORMANCE", "string", None),
    ("setting.mat_vsync", "0", "VSync", "VID: PERFORMANCE", "choice", ["0", "1"]),
    ("setting.r_low_latency", "1", "NVIDIA Reflex: 0=Off 1=On 2=On+Boost", "VID: PERFORMANCE", "choice", ["0", "1", "2"]),
    # ═══ UPSCALING ═══
    ("setting.mat_viewportscale", "0.500000", "Internal render scale (1.0=native)", "VID: UPSCALING", "string", None),
    ("setting.r_citadel_antialiasing", "0", "Anti-aliasing (0=Off if using DLSS)", "VID: UPSCALING", "choice", ["0", "1"]),
    ("setting.r_citadel_upscaling", "4", "0=Off 2=FSR2 4=DLSS", "VID: UPSCALING", "choice", ["0", "2", "4"]),
    ("setting.r_citadel_dlss_settings_mode", "1", "DLSS: 0=Off 1=On", "VID: UPSCALING", "choice", ["0", "1"]),
    ("setting.r_dlss_preset", "10", "DLSS model: 0=Default/CNN 10=Transformer", "VID: UPSCALING", "choice", ["0", "10"]),
    ("setting.r_citadel_fsr_rcas_sharpness", "0.250000", "FSR sharpness", "VID: UPSCALING", "string", None),
    ("setting.r_citadel_fsr2_sharpness", "0.500000", "FSR2 sharpness", "VID: UPSCALING", "string", None),
    ("setting.r_texture_stream_mip_bias", "4", "Texture quality: 2=Smooth 4=Hybrid", "VID: UPSCALING", "choice", ["0", "2", "4"]),
    # ═══ GRAPHICS ═══
    ("setting.r_effects_bloom", "false", "Effects bloom", "VID: GRAPHICS", "string", None),
    ("setting.r_post_bloom", "false", "Post-process bloom", "VID: GRAPHICS", "string", None),
    ("setting.r_depth_of_field", "false", "Depth of field", "VID: GRAPHICS", "string", None),
    ("setting.r_citadel_motion_blur", "0", "Motion blur", "VID: GRAPHICS", "choice", ["0", "1"]),
    ("setting.r_reduce_flash", "1", "Reduce flash effects", "VID: GRAPHICS", "choice", ["0", "1"]),
    ("setting.r_shadows", "0", "Dynamic shadows", "VID: GRAPHICS", "choice", ["0", "1"]),
    ("setting.r_citadel_shadow_quality", "0", "Shadow quality", "VID: GRAPHICS", "choice", ["0", "1", "2", "3"]),
    ("setting.csm_max_shadow_dist_override", "0", "CSM max distance", "VID: GRAPHICS", "string", None),
    ("setting.csm_max_num_cascades_override", "0", "CSM max cascades", "VID: GRAPHICS", "string", None),
    ("setting.csm_viewmodel_shadows", "0", "Viewmodel shadows", "VID: GRAPHICS", "choice", ["0", "1"]),
    ("setting.lb_enable_shadow_casting", "false", "Light shadow casting", "VID: GRAPHICS", "string", None),
    ("setting.lb_dynamic_shadow_resolution", "false", "Dynamic shadow resolution", "VID: GRAPHICS", "string", None),
    ("setting.r_area_lights", "0", "Area lights", "VID: GRAPHICS", "choice", ["0", "1"]),
    ("setting.r_citadel_ssao", "0", "SSAO", "VID: GRAPHICS", "choice", ["0", "1"]),
    ("setting.r_citadel_ssao_quality", "0", "SSAO quality", "VID: GRAPHICS", "choice", ["0", "1", "2", "3"]),
    ("setting.r_citadel_distancefield_ao_quality", "0", "Distance field AO quality", "VID: GRAPHICS", "choice", ["0", "1", "2"]),
    ("setting.r_citadel_fog_quality", "0", "Fog quality", "VID: GRAPHICS", "choice", ["0", "1", "2"]),
    ("setting.shaderquality", "1", "Shader quality", "VID: GRAPHICS", "choice", ["0", "1"]),
    ("setting.r_displacement_mapping", "0", "Displacement mapping", "VID: GRAPHICS", "choice", ["0", "1"]),
    ("setting.r_dashboard_render_quality", "1", "Dashboard render quality", "VID: GRAPHICS", "choice", ["0", "1"]),
    # ═══ VID PARTICLES ═══
    ("setting.r_particle_max_detail_level", "0", "Particle detail level", "VID: PARTICLES", "choice", ["0", "1", "2", "3"]),
    ("setting.r_particle_shadows", "0", "Particle shadows", "VID: PARTICLES", "choice", ["0", "1"]),
    ("setting.r_particle_cables_cast_shadows", "0", "Cable particle shadows", "VID: PARTICLES", "choice", ["0", "1"]),
    ("setting.r_particle_depth_feathering", "false", "Particle depth feathering", "VID: PARTICLES", "string", None),
    ("setting.r_citadel_half_res_noisy_effects", "true", "Half-res noisy effects", "VID: PARTICLES", "string", None),
    ("setting.cl_particle_fallback_base", "4", "Particle fallback base", "VID: PARTICLES", "string", None),
    ("setting.cl_particle_fallback_multiplier", "4", "Particle fallback multiplier", "VID: PARTICLES", "string", None),
    # ═══ MISC ═══
    ("setting.r_citadel_outlines", "1", "Outlines", "VID: MISC", "choice", ["0", "1"]),
    ("setting.r_light_sensitivity_mode", "true", "Light sensitivity mode", "VID: MISC", "string", None),
    ("setting.r_distancefield_enable", "true", "Distance field", "VID: MISC", "string", None),
    ("setting.useadvanced", "1", "Use advanced video settings", "VID: MISC", "choice", ["0", "1"]),
    ("setting.knowndevice", "0", "Known device flag", "VID: MISC", "string", None),
    ("setting.coop_fullscreen", "0", "Co-op fullscreen", "VID: MISC", "choice", ["0", "1"]),
]

VIDEO_CATEGORIES = [
    "VID: DEVICE", "VID: DISPLAY", "VID: PERFORMANCE",
    "VID: UPSCALING", "VID: GRAPHICS", "VID: PARTICLES", "VID: MISC",
]

# ─── COLORS ──────────────────────────────────────────────────────────────────
C_BG          = "#0A0A0A"
C_PANEL       = "#111111"
C_ACCENT      = "#FF3300"
C_ACCENT2     = "#00CCFF"
C_ACCENT3     = "#FFCC00"
C_TEXT        = "#E0E0E0"
C_TEXT_DIM    = "#666666"
C_TEXT_BRIGHT = "#FFFFFF"
C_ENTRY_BG    = "#1A1A1A"
C_BORDER      = "#333333"
C_HOVER       = "#222222"
C_ON          = "#00FF66"
C_SIDEBAR_BG  = "#0D0D0D"
C_SCROLLBAR   = "#333333"
C_VID_ACCENT  = "#CC00FF"


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def find_deadlock_path():
    """Return the Deadlock citadel directory, or None."""
    candidates = [
        r"C:\Program Files (x86)\Steam\steamapps\common\Deadlock\game\citadel",
        r"C:\Program Files\Steam\steamapps\common\Deadlock\game\citadel",
        r"D:\Steam\steamapps\common\Deadlock\game\citadel",
        r"D:\SteamLibrary\steamapps\common\Deadlock\game\citadel",
        r"E:\Steam\steamapps\common\Deadlock\game\citadel",
        r"E:\SteamLibrary\steamapps\common\Deadlock\game\citadel",
        r"F:\Steam\steamapps\common\Deadlock\game\citadel",
        r"F:\SteamLibrary\steamapps\common\Deadlock\game\citadel",
    ]
    home = os.path.expanduser("~")
    candidates += [
        os.path.join(home, ".steam", "steam", "steamapps", "common", "Deadlock", "game", "citadel"),
        os.path.join(home, ".local", "share", "Steam", "steamapps", "common", "Deadlock", "game", "citadel"),
    ]
    for p in candidates:
        if os.path.isdir(p):
            return p
    # Parse libraryfolders.vdf
    vdf_paths = [
        r"C:\Program Files (x86)\Steam\steamapps\libraryfolders.vdf",
        r"C:\Program Files\Steam\steamapps\libraryfolders.vdf",
        os.path.join(home, ".steam", "steam", "steamapps", "libraryfolders.vdf"),
    ]
    for vdf in vdf_paths:
        if not os.path.isfile(vdf):
            continue
        try:
            with open(vdf, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    m = re.search(r'"path"\s+"([^"]+)"', line)
                    if m:
                        citadel = os.path.join(m.group(1), "steamapps", "common",
                                               "Deadlock", "game", "citadel")
                        if os.path.isdir(citadel):
                            return citadel
        except Exception:
            continue
    return None


# ─── TOGGLE WIDGET ────────────────────────────────────────────────────────────

class TDRToggle(tk.Canvas):
    def __init__(self, master, variable, **kw):
        super().__init__(master, width=44, height=20, bg=C_PANEL,
                         highlightthickness=0, cursor="hand2", **kw)
        self.variable = variable
        self._draw()
        self.bind("<Button-1>", self._toggle)
        self.variable.trace_add("write", lambda *_: self._draw())

    def _draw(self):
        self.delete("all")
        val = self.variable.get()
        is_on = val in ("1", "true", "True")
        bg = C_ON if is_on else "#2A2A2A"
        self.create_rectangle(0, 4, 44, 18, fill=bg, outline="")
        x = 30 if is_on else 2
        self.create_rectangle(x, 1, x + 14, 21,
                              fill=C_TEXT_BRIGHT if is_on else C_TEXT_DIM, outline="")

    def _toggle(self, event=None):
        val = self.variable.get()
        is_on = val in ("1", "true", "True")
        if val in ("true", "false"):
            self.variable.set("false" if is_on else "true")
        else:
            self.variable.set("0" if is_on else "1")


# ─── MAIN APP ────────────────────────────────────────────────────────────────

class OptLockApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YEWD'S OPTIMIZER")
        self.geometry("1100x720")
        self.minsize(900, 600)
        self.configure(bg=C_BG)

        # Tell tkinter to use DPI scaling
        try:
            self.tk.call('tk', 'scaling', self.winfo_fpixels('1i') / 72.0)
        except Exception:
            pass

        # Set window icon (taskbar + title bar)
        self._set_icon()

        self.citadel_dir = None
        self.gameinfo_path = None
        self.gameinfo_content = None
        self.video_path = None
        self.video_content = None
        self.cvar_vars = {}
        self.active_tab = "GAMEINFO"
        self.active_category = None

        self._load_fonts()
        self._build_ui()
        self._populate_sidebar()
        self._select_category(GAMEINFO_CATEGORIES[0])
        self.after(100, self._auto_load)

    def _set_icon(self):
        """Set window icon from bundled .ico / .png file."""
        ico_path = resource_path("icon.ico")
        png_path = resource_path("icon.png")
        try:
            if sys.platform == "win32" and os.path.isfile(ico_path):
                self.iconbitmap(ico_path)
            elif os.path.isfile(png_path):
                icon = tk.PhotoImage(file=png_path)
                self.iconphoto(True, icon)
                self._icon_ref = icon  # prevent garbage collection
        except Exception:
            pass

    # ── FONTS ─────────────────────────────────────────────────────────────────

    def _load_fonts(self):
        font_dir = resource_path("fonts")
        self.font_loaded = False
        try:
            if os.path.isdir(font_dir) and sys.platform == "win32":
                import ctypes
                for fn in os.listdir(font_dir):
                    ctypes.windll.gdi32.AddFontResourceExW(
                        os.path.join(font_dir, fn), 0x10, 0)
                self.font_loaded = True
        except Exception:
            pass
        fam = "Helvetica Neue" if self.font_loaded else "Helvetica"
        available = tkfont.families()
        if fam not in available:
            for c in ["Helvetica Neue", "Helvetica", "Arial", "Segoe UI"]:
                if c in available:
                    fam = c
                    break
        self.F_HEADER    = (fam, 18, "bold")
        self.F_SUBHEADER = (fam, 10, "bold")
        self.F_BODY      = (fam, 9)
        self.F_BODY_BOLD = (fam, 9, "bold")
        self.F_SMALL     = (fam, 8)
        self.F_TINY      = (fam, 7)
        self.F_CAT       = (fam, 9, "bold")
        self.F_BRAND     = (fam, 24, "bold")
        self.F_BRAND_SUB = (fam, 8)
        self.F_TAB       = (fam, 10, "bold")

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # TOP BAR
        top = tk.Frame(self, bg=C_BG, height=80)
        top.pack(fill="x", side="top")
        top.pack_propagate(False)

        brand = tk.Frame(top, bg=C_ACCENT)
        brand.pack(side="left", fill="y")
        tk.Label(brand, text="  YEWD'S OPTIMIZER  ", font=self.F_BRAND,
                 bg=C_ACCENT, fg=C_TEXT_BRIGHT).pack(side="left", padx=(8, 0), pady=8)
        vf = tk.Frame(brand, bg=C_ACCENT)
        vf.pack(side="left", padx=(0, 12))
        tk.Label(vf, text="DEADLOCK CONFIG", font=self.F_BRAND_SUB,
                 bg=C_ACCENT, fg="#FFE0D0").pack(anchor="w")
        tk.Label(vf, text="v1.4.3", font=self.F_TINY,
                 bg=C_ACCENT, fg="#FFE0D0").pack(anchor="w")

        stripe = tk.Canvas(top, width=30, height=80, bg=C_BG, highlightthickness=0)
        stripe.pack(side="left")
        stripe.create_polygon(0, 0, 30, 0, 0, 80, fill=C_ACCENT, outline="")

        info = tk.Frame(top, bg=C_BG)
        info.pack(side="left", fill="both", expand=True, padx=16)
        self.status_label = tk.Label(info, text="DETECTING INSTALL...",
                                     font=self.F_SUBHEADER, bg=C_BG, fg=C_ACCENT)
        self.status_label.pack(anchor="w", pady=(14, 2))
        self.path_label = tk.Label(info, text="", font=self.F_SMALL,
                                   bg=C_BG, fg=C_TEXT_DIM)
        self.path_label.pack(anchor="w")
        self.mod_label = tk.Label(info, text="", font=self.F_TINY,
                                  bg=C_BG, fg=C_ACCENT2)
        self.mod_label.pack(anchor="w")

        btns = tk.Frame(top, bg=C_BG)
        btns.pack(side="right", padx=12, pady=12)
        tk.Button(btns, text="► LOCATE", font=self.F_BODY_BOLD,
                  bg=C_ACCENT2, fg=C_BG, relief="flat", cursor="hand2",
                  activebackground="#009FCC", command=self._manual_locate,
                  padx=14, pady=6).pack(side="left", padx=4)
        self.btn_save = tk.Button(btns, text="■ SAVE", font=self.F_BODY_BOLD,
                                  bg=C_ACCENT, fg=C_TEXT_BRIGHT, relief="flat",
                                  cursor="hand2", activebackground="#CC2200",
                                  command=self._save_current, padx=14, pady=6,
                                  state="disabled")
        self.btn_save.pack(side="left", padx=4)
        tk.Button(btns, text="↺ DEFAULTS", font=self.F_BODY_BOLD,
                  bg=C_BORDER, fg=C_TEXT, relief="flat", cursor="hand2",
                  activebackground="#444444", command=self._reset_defaults,
                  padx=14, pady=6).pack(side="left", padx=4)

        # TAB BAR
        tk.Frame(self, bg=C_ACCENT, height=2).pack(fill="x")
        tbar = tk.Frame(self, bg="#0E0E0E", height=32)
        tbar.pack(fill="x")
        tbar.pack_propagate(False)

        self.tab_gi = tk.Label(tbar, text="  GAMEINFO.GI  ", font=self.F_TAB,
                               bg=C_ACCENT, fg=C_TEXT_BRIGHT, cursor="hand2",
                               padx=16, pady=4)
        self.tab_gi.pack(side="left")
        self.tab_gi.bind("<Button-1>", lambda e: self._switch_tab("GAMEINFO"))

        self.tab_vid = tk.Label(tbar, text="  VIDEO.TXT  ", font=self.F_TAB,
                                bg="#0E0E0E", fg=C_TEXT_DIM, cursor="hand2",
                                padx=16, pady=4)
        self.tab_vid.pack(side="left")
        self.tab_vid.bind("<Button-1>", lambda e: self._switch_tab("VIDEO"))

        self.vid_dot = tk.Label(tbar, text="", font=self.F_TINY,
                                bg="#0E0E0E", fg=C_TEXT_DIM)
        self.vid_dot.pack(side="left", padx=8)

        tk.Frame(self, bg=C_BORDER, height=1).pack(fill="x")

        # MAIN CONTENT
        main = tk.Frame(self, bg=C_BG)
        main.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(main, bg=C_SIDEBAR_BG, width=185)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        tk.Label(self.sidebar, text="CATEGORIES", font=self.F_TINY,
                 bg=C_SIDEBAR_BG, fg=C_TEXT_DIM).pack(anchor="w", padx=12, pady=(12, 6))
        tk.Frame(self.sidebar, bg=C_BORDER, height=1).pack(fill="x", padx=8)
        self.cat_buttons = {}

        cf = tk.Frame(main, bg=C_BG)
        cf.pack(side="left", fill="both", expand=True)
        self.canvas = tk.Canvas(cf, bg=C_BG, highlightthickness=0)
        sb = tk.Scrollbar(cf, orient="vertical", command=self.canvas.yview,
                          bg=C_SCROLLBAR, troughcolor=C_BG, width=8, relief="flat")
        self.canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.inner = tk.Frame(self.canvas, bg=C_BG)
        self.cwin = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>",
                        lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>",
                         lambda e: self.canvas.itemconfig(self.cwin, width=e.width))
        self.canvas.bind_all("<MouseWheel>",
                             lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))

        # BOTTOM BAR
        bot = tk.Frame(self, bg=C_PANEL, height=28)
        bot.pack(fill="x", side="bottom")
        bot.pack_propagate(False)
        self.bot_status = tk.Label(bot, text="OPTIMIZATIONLOCK v1.4.3",
                                   font=self.F_TINY, bg=C_PANEL, fg=C_TEXT_DIM)
        self.bot_status.pack(side="left", padx=12)
        self.bot_backup = tk.Label(bot, text="", font=self.F_TINY,
                                   bg=C_PANEL, fg=C_TEXT_DIM)
        self.bot_backup.pack(side="right", padx=12)

    # ── TABS ──────────────────────────────────────────────────────────────────

    def _switch_tab(self, tab):
        self.active_tab = tab
        if tab == "GAMEINFO":
            self.tab_gi.configure(bg=C_ACCENT, fg=C_TEXT_BRIGHT)
            self.tab_vid.configure(bg="#0E0E0E", fg=C_TEXT_DIM)
        else:
            self.tab_gi.configure(bg="#0E0E0E", fg=C_TEXT_DIM)
            self.tab_vid.configure(bg=C_VID_ACCENT, fg=C_TEXT_BRIGHT)
        self._populate_sidebar()
        cats = GAMEINFO_CATEGORIES if tab == "GAMEINFO" else VIDEO_CATEGORIES
        self._select_category(cats[0])

    # ── SIDEBAR ───────────────────────────────────────────────────────────────

    def _populate_sidebar(self):
        for b in self.cat_buttons.values():
            b.destroy()
        self.cat_buttons.clear()

        if self.active_tab == "GAMEINFO":
            cats, settings, ci = GAMEINFO_CATEGORIES, CONVARS, 4
        else:
            cats, settings, ci = VIDEO_CATEGORIES, VIDEO_SETTINGS, 3

        for cat in cats:
            n = sum(1 for s in settings if s[ci] == cat)
            if n == 0:
                continue
            label = cat.replace("VID: ", "") if cat.startswith("VID: ") else cat
            btn = tk.Label(self.sidebar, text=f"  {label}  ({n})",
                          font=self.F_CAT, bg=C_SIDEBAR_BG, fg=C_TEXT_DIM,
                          anchor="w", padx=12, pady=6, cursor="hand2")
            btn.pack(fill="x")
            btn.bind("<Button-1>", lambda e, c=cat: self._select_category(c))
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=C_HOVER)
                     if b != self.cat_buttons.get(self.active_category) else None)
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=C_SIDEBAR_BG)
                     if b != self.cat_buttons.get(self.active_category) else None)
            self.cat_buttons[cat] = btn

    # ── CATEGORY VIEW ─────────────────────────────────────────────────────────

    def _select_category(self, category):
        accent = C_ACCENT if self.active_tab == "GAMEINFO" else C_VID_ACCENT
        for cat, btn in self.cat_buttons.items():
            btn.configure(bg=(accent if cat == category else C_SIDEBAR_BG),
                          fg=(C_TEXT_BRIGHT if cat == category else C_TEXT_DIM))
        self.active_category = category

        for w in self.inner.winfo_children():
            w.destroy()

        is_gi = self.active_tab == "GAMEINFO"
        settings = CONVARS if is_gi else VIDEO_SETTINGS
        # tuple indices differ: CONVARS=(name,val,def,desc,cat,type,opts)
        #                        VIDEO =(name,val,desc,cat,type,opts)

        label = category.replace("VID: ", "") if category.startswith("VID: ") else category
        hdr = tk.Frame(self.inner, bg=C_BG)
        hdr.pack(fill="x", padx=20, pady=(16, 4))
        tk.Label(hdr, text=f"◆ {label}", font=self.F_HEADER,
                 bg=C_BG, fg=C_TEXT_BRIGHT).pack(side="left")
        tk.Frame(self.inner, bg=accent, height=1).pack(fill="x", padx=20, pady=(0, 12))

        for s in settings:
            if is_gi:
                name, rec, defv, desc, cat, vtype, opts = s
            else:
                name, rec, desc, cat, vtype, opts = s
                defv = None

            if cat != category:
                continue

            if name not in self.cvar_vars:
                self.cvar_vars[name] = tk.StringVar(value=rec)
            var = self.cvar_vars[name]

            row = tk.Frame(self.inner, bg=C_PANEL, padx=16, pady=10)
            row.pack(fill="x", padx=20, pady=2)

            left = tk.Frame(row, bg=C_PANEL)
            left.pack(side="left", fill="x", expand=True)
            tk.Label(left, text=name, font=self.F_BODY_BOLD,
                     bg=C_PANEL, fg=C_ACCENT2).pack(anchor="w")
            tk.Label(left, text=desc, font=self.F_SMALL,
                     bg=C_PANEL, fg=C_TEXT_DIM).pack(anchor="w")
            if defv is not None:
                tk.Label(left, text=f"DEFAULT: {defv}", font=self.F_TINY,
                         bg=C_PANEL, fg="#444444").pack(anchor="w")
            else:
                tk.Label(left, text=f"RECOMMENDED: {rec}", font=self.F_TINY,
                         bg=C_PANEL, fg="#444444").pack(anchor="w")

            right = tk.Frame(row, bg=C_PANEL)
            right.pack(side="right", padx=(12, 0))

            if vtype in ("bool", "bool_str"):
                TDRToggle(right, var).pack(pady=4)
            elif vtype == "choice":
                cb = ttk.Combobox(right, textvariable=var, values=opts,
                                  state="readonly", width=8, font=self.F_BODY)
                cb.pack(pady=4)
                self._style_combo()
            elif vtype in ("int", "float"):
                cf = tk.Frame(right, bg=C_PANEL)
                cf.pack(pady=4)
                tk.Entry(cf, textvariable=var, font=self.F_BODY,
                         bg=C_ENTRY_BG, fg=C_TEXT_BRIGHT, insertbackground=C_ACCENT,
                         relief="flat", width=8, justify="center",
                         highlightthickness=1, highlightcolor=C_ACCENT,
                         highlightbackground=C_BORDER).pack(side="left")
                if opts:
                    tk.Label(cf, text=f"[{opts[0]}–{opts[1]}]", font=self.F_TINY,
                             bg=C_PANEL, fg=C_TEXT_DIM).pack(side="left", padx=(6, 0))
            else:
                tk.Entry(right, textvariable=var, font=self.F_BODY,
                         bg=C_ENTRY_BG, fg=C_TEXT_BRIGHT, insertbackground=C_ACCENT,
                         relief="flat", width=14, justify="center",
                         highlightthickness=1, highlightcolor=C_ACCENT,
                         highlightbackground=C_BORDER).pack(pady=4)

            reset_val = defv if defv is not None else rec
            rst = tk.Label(right, text="↺", font=(self.F_BODY[0], 12),
                          bg=C_PANEL, fg=C_TEXT_DIM, cursor="hand2")
            rst.pack(side="right", padx=(8, 0))
            rst.bind("<Button-1>", lambda e, v=var, d=reset_val: v.set(d))
            rst.bind("<Enter>", lambda e, l=rst: l.configure(fg=C_ACCENT))
            rst.bind("<Leave>", lambda e, l=rst: l.configure(fg=C_TEXT_DIM))

        self.canvas.yview_moveto(0)

    def _style_combo(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("TCombobox", fieldbackground=C_ENTRY_BG, background=C_BORDER,
                    foreground=C_TEXT_BRIGHT, arrowcolor=C_TEXT, borderwidth=0)
        s.map("TCombobox", fieldbackground=[("readonly", C_ENTRY_BG)],
              selectbackground=[("readonly", C_ENTRY_BG)],
              selectforeground=[("readonly", C_TEXT_BRIGHT)])

    # ── AUTO-LOAD ─────────────────────────────────────────────────────────────

    def _auto_load(self):
        self.citadel_dir = find_deadlock_path()
        if not self.citadel_dir:
            self.status_label.configure(text="AUTO-DETECT FAILED", fg=C_ACCENT3)
            self.path_label.configure(text="Use LOCATE to find your Deadlock citadel folder",
                                      fg=C_TEXT_DIM)
            return
        self._load_from_dir(self.citadel_dir)

    def _manual_locate(self):
        d = filedialog.askdirectory(title="Select Deadlock citadel folder "
                                    "(steamapps/common/Deadlock/game/citadel)")
        if not d:
            return
        self.citadel_dir = d
        self._load_from_dir(d)

    def _load_from_dir(self, d):
        self.status_label.configure(text="INSTALL FOUND", fg=C_ON)
        self.path_label.configure(text=d, fg=C_TEXT)
        backups = []

        gi = os.path.join(d, "gameinfo.gi")
        if os.path.isfile(gi):
            self._load_file(gi, "gameinfo")
            backups.append("gameinfo.gi")

        vt = os.path.join(d, "cfg", "video.txt")
        if os.path.isfile(vt):
            self._load_file(vt, "video")
            self.vid_dot.configure(text="● video.txt loaded", fg=C_ON)
            backups.append("video.txt")
        else:
            self.vid_dot.configure(text="○ video.txt not found in cfg/", fg=C_ACCENT3)

        if backups:
            self.bot_backup.configure(
                text="BACKUPS: " + ", ".join(f"{b}.backup_original" for b in backups))

        self.btn_save.configure(state="normal")
        if self.active_category:
            self._select_category(self.active_category)

    def _load_file(self, path, kind):
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read {path}:\n{e}")
            return
        backup = path + ".backup_original"
        if not os.path.exists(backup):
            try:
                shutil.copy2(path, backup)
            except Exception:
                pass
        if kind == "gameinfo":
            self.gameinfo_path = path
            self.gameinfo_content = content
            self._parse_gameinfo(content)
        else:
            self.video_path = path
            self.video_content = content
            self._parse_video(content)

    # ── PARSING ───────────────────────────────────────────────────────────────

    def _parse_gameinfo(self, content):
        for cvar in CONVARS:
            name = cvar[0]
            for line in content.split("\n"):
                s = line.strip()
                if s.startswith("//"):
                    continue
                m = re.match(rf'^\s*{re.escape(name)}\s+"([^"]*)"', s)
                if not m:
                    m = re.match(rf'^\s*{re.escape(name)}\s+(\S+)', s)
                if m:
                    val = m.group(1).strip()
                    if name in self.cvar_vars:
                        self.cvar_vars[name].set(val)
                    else:
                        self.cvar_vars[name] = tk.StringVar(value=val)
                    break

    def _parse_video(self, content):
        for vs in VIDEO_SETTINGS:
            name = vs[0]
            for line in content.split("\n"):
                s = line.strip()
                if s.startswith("//"):
                    continue
                m = re.match(rf'^\s*"{re.escape(name)}"\s+"([^"]*)"', s)
                if m:
                    val = m.group(1).strip()
                    if name in self.cvar_vars:
                        self.cvar_vars[name].set(val)
                    else:
                        self.cvar_vars[name] = tk.StringVar(value=val)
                    break

    # ── SAVE ──────────────────────────────────────────────────────────────────

    def _save_current(self):
        saved = []
        if self.gameinfo_path and self.gameinfo_content:
            if self._save_gameinfo():
                saved.append("gameinfo.gi")
        if self.video_path and self.video_content:
            if self._save_video():
                saved.append("video.txt")
        if saved:
            self.status_label.configure(text="SAVED", fg=C_ON)
            self.bot_status.configure(text=f"SAVED: {', '.join(saved)}")
        else:
            messagebox.showerror("Error", "No files loaded to save.")

    def _save_gameinfo(self):
        lines = self.gameinfo_content.split("\n")
        out = []
        for line in lines:
            s = line.strip()
            if s.startswith("//"):
                out.append(line)
                continue
            done = False
            for cvar in CONVARS:
                name = cvar[0]
                if name not in self.cvar_vars:
                    continue
                m = re.match(rf'^(\s*){re.escape(name)}(\s+)"([^"]*)"(.*)', s)
                if not m:
                    m = re.match(rf'^(\s*){re.escape(name)}(\s+)(\S+)(.*)', s)
                if m:
                    nv = self.cvar_vars[name].get()
                    sp, ov, rest = m.group(2), m.group(3), m.group(4)
                    ws = ""
                    for ch in line:
                        if ch in (" ", "\t"):
                            ws += ch
                        else:
                            break
                    vs = f'"{nv}"' if ('"' + ov + '"') in s else nv
                    out.append(f"{ws}{name}{sp}{vs}{rest}")
                    done = True
                    break
            if not done:
                out.append(line)
        try:
            with open(self.gameinfo_path, "w", encoding="utf-8") as f:
                f.write("\n".join(out))
            self.gameinfo_content = "\n".join(out)
            return True
        except PermissionError:
            messagebox.showerror("Permission Denied",
                                 f"Cannot write to:\n{self.gameinfo_path}\n\nRun as Administrator.")
        except Exception as e:
            messagebox.showerror("Error", f"gameinfo.gi save failed:\n{e}")
        return False

    def _save_video(self):
        lines = self.video_content.split("\n")
        out = []
        for line in lines:
            s = line.strip()
            if s.startswith("//"):
                out.append(line)
                continue
            done = False
            for vs in VIDEO_SETTINGS:
                name = vs[0]
                if name not in self.cvar_vars:
                    continue
                m = re.match(rf'^(\s*)"{re.escape(name)}"(\s+)"([^"]*)"(.*)', s)
                if m:
                    nv = self.cvar_vars[name].get()
                    sp, rest = m.group(2), m.group(4)
                    ws = ""
                    for ch in line:
                        if ch in (" ", "\t"):
                            ws += ch
                        else:
                            break
                    out.append(f'{ws}"{name}"{sp}"{nv}"{rest}')
                    done = True
                    break
            if not done:
                out.append(line)
        try:
            with open(self.video_path, "w", encoding="utf-8") as f:
                f.write("\n".join(out))
            self.video_content = "\n".join(out)
            return True
        except PermissionError:
            messagebox.showerror("Permission Denied",
                                 f"Cannot write to:\n{self.video_path}\n\nRun as Administrator.")
        except Exception as e:
            messagebox.showerror("Error", f"video.txt save failed:\n{e}")
        return False

    # ── RESET ─────────────────────────────────────────────────────────────────

    def _reset_defaults(self):
        if self.active_tab == "GAMEINFO":
            if not messagebox.askyesno("Reset", "Reset ALL gameinfo values to OptimizationLock defaults?"):
                return
            for cvar in CONVARS:
                if cvar[0] in self.cvar_vars:
                    self.cvar_vars[cvar[0]].set(cvar[1])
        else:
            if not messagebox.askyesno("Reset", "Reset ALL video values to recommended defaults?\n"
                                       "(VendorID and DeviceID will NOT be changed)"):
                return
            for vs in VIDEO_SETTINGS:
                name, val = vs[0], vs[1]
                if name in ("VendorID", "DeviceID"):
                    continue  # never reset device IDs
                if name in self.cvar_vars and val:
                    self.cvar_vars[name].set(val)
        self.mod_label.configure(text="ALL VALUES RESET")
        if self.active_category:
            self._select_category(self.active_category)


if __name__ == "__main__":
    app = OptLockApp()
    app.mainloop()
