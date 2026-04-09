#!/usr/bin/env python3
"""
YEWD'S OPTIMIZER v1.4.3
GUI for editing Deadlock's gameinfo.gi, video.txt, and autoexec.cfg
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font as tkfont
import os, re, shutil, sys

# DPI fix — before tkinter init
if sys.platform == "win32":
    try:
        import ctypes
        a = ctypes.c_int()
        ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(a))
        if a.value == 0:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try: ctypes.windll.user32.SetProcessDPIAware()
        except Exception: pass

# ─── GAMEINFO CONVARS ─────────────────────────────────────────────────────────
CONVARS = [
    ("citadel_trooper_glow_disabled","0","0","Disable friendly/enemy minion glow","OUTLINES","bool",None),
    ("citadel_boss_glow_disabled","1","0","Disable boss and walker glow/highlight","OUTLINES","bool",None),
    ("citadel_player_glow_disabled","0","0","Disable player glow/highlight when pinged","OUTLINES","bool",None),
    ("r_citadel_npr_outlines_max_dist","1000","1000","Outline max render distance","OUTLINES","int",(0,5000)),
    ("citadel_camera_hero_fov","110","90","Camera FOV when following hero","FOV","int",(70,130)),
    ("citadel_unit_status_use_new","1","0","Use new health bar style","HUD","bool",None),
    ("citadel_hud_objective_health_enabled","2","2","Obj health: 0=Off 1=Shrines 2=T1/T2 3=Barracks","HUD","choice",["0","1","2","3"]),
    ("citadel_damage_report_enable","1","1","Enable incoming/outgoing damage tab","HUD","bool",None),
    ("citadel_hideout_ball_show_juggle_count","1","0","Show hideout ball juggle counter","HUD","bool",None),
    ("citadel_hideout_ball_show_juggle_fx","1","0","Show juggle visual FX","HUD","bool",None),
    ("citadel_crosshair_hit_marker_duration","-0.001","0.1","Hitmarker duration (-0.001 to remove)","HUD","float",(-0.001,1.0)),
    ("lb_enable_stationary_lights","1","1","Stationary lights","LIGHTING","bool",None),
    ("lb_enable_dynamic_lights","0","1","Dynamic lights (walker, shop, abilities)","LIGHTING","bool",None),
    ("lb_enable_baked_shadows","1","1","Baked shadows","LIGHTING","bool",None),
    ("r_drawskybox","1","1","Draw 2D skybox","SKYBOX","bool",None),
    ("r_draw3dskybox","0","1","Draw 3D skybox layer","SKYBOX","bool",None),
    ("fps_max","0","400","Max FPS in-game (0=unlimited)","FPS","int",(0,999)),
    ("engine_no_focus_sleep","20","20","Sleep ms when unfocused","FPS","int",(0,100)),
    ("engine_low_latency_sleep_after_client_tick","1","0","Low-latency sleep after client tick","FPS","bool",None),
    ("panorama_max_fps","15","120","Menu/UI FPS cap","FPS","int",(0,240)),
    ("panorama_max_overlay_fps","15","60","Overlay FPS cap","FPS","int",(0,240)),
    ("r_size_cull_threshold","0.7","0.8","Small object cull threshold","CULLING","float",(0.0,2.0)),
    ("r_citadel_clip_sphere_min_opacity","0","40","Pinhole camera blur (0=off)","CAMERA","int",(0,100)),
    ("r_citadel_enable_pano_world_blur","false","true","Panorama world blur","UI","bool_str",None),
    ("r_dashboard_render_quality","0","1","Dashboard render quality","UI","choice",["0","1"]),
    ("panorama_disable_box_shadow","1","0","Disable UI box shadows","UI","bool",None),
    ("panorama_disable_blur","1","0","Disable UI blur effects","UI","bool",None),
    ("panorama_allow_transitions","false","1","UI animations (shop etc)","UI","bool_str",None),
    ("closecaption","false","true","Closed captions","UI","bool_str",None),
    ("r_shadows","0","1","Dynamic shadows","SHADOWS","bool",None),
    ("r_citadel_shadow_quality","0","2","Shadow quality level","SHADOWS","choice",["0","1","2","3"]),
    ("r_citadel_gpu_culling_shadows","1","0","GPU-driven shadow culling","SHADOWS","bool",None),
    ("csm_max_shadow_dist_override","0","1024","CSM max distance override","SHADOWS","int",(0,4096)),
    ("r_size_cull_threshold_shadow","1","0.2","Shadow size cull threshold","SHADOWS","float",(0.0,2.0)),
    ("lb_enable_shadow_casting","0","1","Light shadow casting","SHADOWS","bool",None),
    ("lb_barnlight_shadowmap_scale","0.5","1","Barnlight shadowmap scale","SHADOWS","float",(0.0,2.0)),
    ("lb_csm_cascade_size_override","1","1536","CSM cascade size override","SHADOWS","int",(0,4096)),
    ("lb_csm_override_staticgeo_cascades","0","1","Static geometry cascades","SHADOWS","bool",None),
    ("lb_sun_csm_size_cull_threshold_texels","30","10","CSM texel cull threshold","SHADOWS","int",(0,100)),
    ("lb_dynamic_shadow_resolution_base","256","1536","Dynamic shadow resolution","SHADOWS","int",(64,4096)),
    ("sc_disable_spotlight_shadows","1","0","Disable spotlight shadows","SHADOWS","bool",None),
    ("cl_globallight_shadow_mode","0","2","Global light shadow mode","SHADOWS","choice",["0","1","2"]),
    ("r_directlighting","false","true","Direct lighting","DEEP LIGHTING","bool_str",None),
    ("r_rendersun","0","1","Sun lighting","DEEP LIGHTING","bool",None),
    ("cl_retire_low_priority_lights","1","0","Retire low-priority lights","DEEP LIGHTING","bool",None),
    ("r_lightmap_size","4","65536","Max lightmap resolution","DEEP LIGHTING","int",(4,65536)),
    ("r_lightmap_size_directional_irradiance","4","-1","Directional irradiance lightmap size","DEEP LIGHTING","int",(-1,65536)),
    ("r_ssao","0","1","Screen-space ambient occlusion","DEEP LIGHTING","bool",None),
    ("r_ssao_strength","0","1.2","SSAO strength","DEEP LIGHTING","float",(0.0,3.0)),
    ("r_citadel_ssao_quality","0","3","SSAO quality level","DEEP LIGHTING","choice",["0","1","2","3"]),
    ("mat_set_shader_quality","0","null","Shader quality (0 or 1)","DEEP LIGHTING","choice",["0","1"]),
    ("r_distancefield_enable","0","1","Distance field system","DEEP LIGHTING","bool",None),
    ("r_citadel_distancefield_farfield_enable","0","1","Far-field distance field","DEEP LIGHTING","bool",None),
    ("skeleton_instance_lod_optimization","1","0","Skeleton LOD optimization","MODELS","bool",None),
    ("enable_boneflex","0","1","Bone flex (facial/mesh flex)","MODELS","bool",None),
    ("r_hair_ao","0","1","Hair ambient occlusion","MODELS","bool",None),
    ("ik_final_fixup_enable","0","1","Final IK fixup pass","MODELS","bool",None),
    ("cloth_sim_on_tick","0","1","Cloth sim every tick","MODELS","bool",None),
    ("mat_colorcorrection","1","1","Color correction","VISUAL","bool",None),
    ("r_drawdecals","1","1","Render decals","VISUAL","bool",None),
    ("r_depth_of_field","0","1","Depth of field","VISUAL","bool",None),
    ("r_effects_bloom","0","1","Effects bloom","VISUAL","bool",None),
    ("r_post_bloom","0","1","Post-process bloom","VISUAL","bool",None),
    ("r_enable_volume_fog","0","1","Volumetric fog","VISUAL","bool",None),
    ("r_enable_gradient_fog","0","1","Gradient fog","VISUAL","bool",None),
    ("r_enable_cubemap_fog","0","1","Cubemap fog","VISUAL","bool",None),
    ("r_citadel_fog_quality","0","1","Fog quality level","VISUAL","choice",["0","1","2"]),
    ("cl_show_splashes","0","1","Splash effects","VISUAL","bool",None),
    ("violence_hblood","0","1","Human blood effects","VISUAL","bool",None),
    ("violence_ablood","0","1","Alien blood effects","VISUAL","bool",None),
    ("sc_clutter_enable","0","1","Clutter props (debris)","VISUAL","bool",None),
    ("gpu_level","1","3","GPU level","SYSTEM","choice",["0","1","2","3"]),
    ("gpu_mem_level","1","2","GPU memory level","SYSTEM","choice",["0","1","2"]),
    ("cpu_level","1","2","CPU level","SYSTEM","choice",["0","1","2"]),
    ("r_particle_max_detail_level","0","3","Particle max detail level","PARTICLES","choice",["0","1","2","3"]),
    ("particle_cluster_nodraw","1","0","Skip drawing particle clusters","PARTICLES","bool",None),
    ("r_RainParticleDensity","0","1","Rain particle density","PARTICLES","float",(0.0,1.0)),
    ("r_world_wind_strength","0","40","Wind effects strength","PARTICLES","int",(0,100)),
    ("cl_particle_fallback_multiplier","4","0","Particle fallback aggression","PARTICLES","int",(0,10)),
    ("sc_screen_size_lod_scale_override","0.56","-1","LOD scale","LOD","float",(-1.0,2.0)),
    ("sc_instanced_mesh_lod_bias","15","1.25","Instanced mesh LOD bias","LOD","float",(0.0,30.0)),
    ("sc_fade_distance_scale_override","180","-1","Object fade distance","LOD","int",(-1,500)),
    ("sv_pvs_max_distance","2800","0","Max player render distance","LOD","int",(0,10000)),
    ("mat_viewportscale","0.01","1","Viewport LOD scale","LOD","float",(0.01,1.0)),
    ("r_mapextents","4500","16384","Far clipping plane","LOD","int",(1000,32000)),
    ("r_drawropes","0","1","Draw ropes","ROPES","bool",None),
    ("rope_collide","0","1","Rope collision simulation","ROPES","bool",None),
    ("rope_subdiv","0","2","Rope subdivision quality","ROPES","int",(0,8)),
    ("cl_disable_ragdolls","0","0","Disable ragdolls (can break Doorman ult)","RAGDOLLS","bool",None),
    ("ragdoll_parallel_pose_control","1","0","Multithreaded ragdoll handling","RAGDOLLS","bool",None),
    ("r_grass_quality","0","2","Grass quality","GRASS","choice",["0","1","2"]),
    ("r_grass_start_fade","0","0","Grass close fade distance","GRASS","int",(0,500)),
    ("r_grass_end_fade","0","300","Grass far fade distance","GRASS","int",(0,1000)),
]
GI_CATS = ["FOV","OUTLINES","HUD","LIGHTING","SKYBOX","FPS","SHADOWS","DEEP LIGHTING",
           "UI","VISUAL","MODELS","PARTICLES","CULLING","LOD","ROPES","RAGDOLLS","GRASS","SYSTEM","CAMERA"]

# ─── VIDEO.TXT ────────────────────────────────────────────────────────────────
VIDEO_SETTINGS = [
    ("VendorID","","GPU vendor: NVIDIA=4318 AMD=4098 Intel=32902","VID: DEVICE","string",None),
    ("DeviceID","","Your GPU model ID (from original video.txt)","VID: DEVICE","string",None),
    ("setting.defaultres","1920","Monitor width","VID: DISPLAY","string",None),
    ("setting.defaultresheight","1080","Monitor height","VID: DISPLAY","string",None),
    ("setting.recommendedheight","1080","Same as defaultresheight","VID: DISPLAY","string",None),
    ("setting.refreshrate_numerator","144","Monitor refresh rate (Hz)","VID: DISPLAY","string",None),
    ("setting.refreshrate_denominator","1","Refresh rate denominator","VID: DISPLAY","string",None),
    ("setting.fullscreen","1","1=Exclusive Fullscreen 0=Borderless","VID: DISPLAY","choice",["0","1"]),
    ("setting.nowindowborder","1","Borderless window","VID: DISPLAY","choice",["0","1"]),
    ("setting.monitor_index","0","0=Primary 1=Second monitor","VID: DISPLAY","choice",["0","1","2"]),
    ("setting.fullscreen_min_on_focus_loss","1","Minimize on focus loss","VID: DISPLAY","choice",["0","1"]),
    ("setting.high_dpi","0","High DPI mode","VID: DISPLAY","choice",["0","1"]),
    ("setting.aspectratiomode","0","Aspect ratio mode","VID: DISPLAY","choice",["0","1","2"]),
    ("setting.r_fullscreen_gamma","2.100000","Fullscreen gamma","VID: DISPLAY","string",None),
    ("setting.cpu_level","1","CPU quality level","VID: PERFORMANCE","choice",["0","1","2","3"]),
    ("setting.gpu_level","1","GPU quality level","VID: PERFORMANCE","choice",["0","1","2","3"]),
    ("setting.mem_level","3","RAM: 4-8GB=1 12-16GB=2 24GB+=3","VID: PERFORMANCE","choice",["1","2","3"]),
    ("setting.gpu_mem_level","3","VRAM: 2-4GB=1 6-8GB=2 12GB+=3","VID: PERFORMANCE","choice",["1","2","3"]),
    ("setting.fps_max","0","FPS cap (0=uncapped)","VID: PERFORMANCE","string",None),
    ("setting.mat_vsync","0","VSync","VID: PERFORMANCE","choice",["0","1"]),
    ("setting.r_low_latency","1","NVIDIA Reflex: 0=Off 1=On 2=On+Boost","VID: PERFORMANCE","choice",["0","1","2"]),
    ("setting.mat_viewportscale","0.500000","Internal render scale (1.0=native)","VID: UPSCALING","string",None),
    ("setting.r_citadel_antialiasing","0","Anti-aliasing (0=Off if using DLSS)","VID: UPSCALING","choice",["0","1"]),
    ("setting.r_citadel_upscaling","4","0=Off 2=FSR2 4=DLSS","VID: UPSCALING","choice",["0","2","4"]),
    ("setting.r_citadel_dlss_settings_mode","1","DLSS: 0=Off 1=On","VID: UPSCALING","choice",["0","1"]),
    ("setting.r_dlss_preset","10","DLSS model: 0=Default/CNN 10=Transformer","VID: UPSCALING","choice",["0","10"]),
    ("setting.r_citadel_fsr_rcas_sharpness","0.250000","FSR sharpness","VID: UPSCALING","string",None),
    ("setting.r_citadel_fsr2_sharpness","0.500000","FSR2 sharpness","VID: UPSCALING","string",None),
    ("setting.r_texture_stream_mip_bias","4","Texture quality: 2=Smooth 4=Hybrid","VID: UPSCALING","choice",["0","2","4"]),
    ("setting.r_effects_bloom","false","Effects bloom","VID: GRAPHICS","string",None),
    ("setting.r_post_bloom","false","Post-process bloom","VID: GRAPHICS","string",None),
    ("setting.r_depth_of_field","false","Depth of field","VID: GRAPHICS","string",None),
    ("setting.r_citadel_motion_blur","0","Motion blur","VID: GRAPHICS","choice",["0","1"]),
    ("setting.r_reduce_flash","1","Reduce flash effects","VID: GRAPHICS","choice",["0","1"]),
    ("setting.r_shadows","0","Dynamic shadows","VID: GRAPHICS","choice",["0","1"]),
    ("setting.r_citadel_shadow_quality","0","Shadow quality","VID: GRAPHICS","choice",["0","1","2","3"]),
    ("setting.csm_max_shadow_dist_override","0","CSM max distance","VID: GRAPHICS","string",None),
    ("setting.csm_max_num_cascades_override","0","CSM max cascades","VID: GRAPHICS","string",None),
    ("setting.csm_viewmodel_shadows","0","Viewmodel shadows","VID: GRAPHICS","choice",["0","1"]),
    ("setting.lb_enable_shadow_casting","false","Light shadow casting","VID: GRAPHICS","string",None),
    ("setting.lb_dynamic_shadow_resolution","false","Dynamic shadow resolution","VID: GRAPHICS","string",None),
    ("setting.r_area_lights","0","Area lights","VID: GRAPHICS","choice",["0","1"]),
    ("setting.r_citadel_ssao","0","SSAO","VID: GRAPHICS","choice",["0","1"]),
    ("setting.r_citadel_ssao_quality","0","SSAO quality","VID: GRAPHICS","choice",["0","1","2","3"]),
    ("setting.r_citadel_distancefield_ao_quality","0","Distance field AO quality","VID: GRAPHICS","choice",["0","1","2"]),
    ("setting.r_citadel_fog_quality","0","Fog quality","VID: GRAPHICS","choice",["0","1","2"]),
    ("setting.shaderquality","1","Shader quality","VID: GRAPHICS","choice",["0","1"]),
    ("setting.r_displacement_mapping","0","Displacement mapping","VID: GRAPHICS","choice",["0","1"]),
    ("setting.r_dashboard_render_quality","1","Dashboard render quality","VID: GRAPHICS","choice",["0","1"]),
    ("setting.r_particle_max_detail_level","0","Particle detail level","VID: PARTICLES","choice",["0","1","2","3"]),
    ("setting.r_particle_shadows","0","Particle shadows","VID: PARTICLES","choice",["0","1"]),
    ("setting.r_particle_cables_cast_shadows","0","Cable particle shadows","VID: PARTICLES","choice",["0","1"]),
    ("setting.r_particle_depth_feathering","false","Particle depth feathering","VID: PARTICLES","string",None),
    ("setting.r_citadel_half_res_noisy_effects","true","Half-res noisy effects","VID: PARTICLES","string",None),
    ("setting.cl_particle_fallback_base","4","Particle fallback base","VID: PARTICLES","string",None),
    ("setting.cl_particle_fallback_multiplier","4","Particle fallback multiplier","VID: PARTICLES","string",None),
    ("setting.r_citadel_outlines","1","Outlines","VID: MISC","choice",["0","1"]),
    ("setting.r_light_sensitivity_mode","true","Light sensitivity mode","VID: MISC","string",None),
    ("setting.r_distancefield_enable","true","Distance field","VID: MISC","string",None),
    ("setting.useadvanced","1","Use advanced video settings","VID: MISC","choice",["0","1"]),
    ("setting.knowndevice","0","Known device flag","VID: MISC","string",None),
    ("setting.coop_fullscreen","0","Co-op fullscreen","VID: MISC","choice",["0","1"]),
]
VID_CATS = ["VID: DEVICE","VID: DISPLAY","VID: PERFORMANCE","VID: UPSCALING","VID: GRAPHICS","VID: PARTICLES","VID: MISC"]

# ─── AUTOEXEC CONFIGS ─────────────────────────────────────────────────────────
NULLS_CFG = r"""bind w +mfwd
bind s +mback
bind a +mleft
bind d +mright

alias +mfwd "-back;+forward;alias checkfwd +forward;"
alias +mback "-forward;+back;alias checkback +back;"
alias +mleft "-moveright;+moveleft;alias checkleft +moveleft;"
alias +mright "-moveleft;+moveright;alias checkright +moveright;"
alias -mfwd "-forward;checkback;alias checkfwd none;"
alias -mback "-back;checkfwd;alias checkback none;"
alias -mleft "-moveleft;checkright;alias checkleft none;"
alias -mright "-moveright;checkleft;alias checkright none;"
alias checkfwd none
alias checkback none
alias checkleft none
alias checkright none
alias none ""
bind "SPACE" "+jump"
bind "ctrl" "+duck"
"""

OPTIMIZED_CFG = r"""// Zoom Sensitivity
zoom_sensitivity_ratio "0.818933027098955175"

// FPS
fps_max "0"
fps_max_tools "60"
fps_max_ui "60"

// Graphics
mat_viewportscale "0.1"

// Deadlock cl_ statements
cl_auto_cursor_scale "false"
cl_lagcompensation "true"
cl_ragdoll_limit "0"
cl_tickpacket_desired_queuelength "1"

// Graphics and Performance
r_low_latency "1"
engine_low_latency_sleep_after_client_tick "false"
r_drawtracers_firstperson "false"

// Network
cl_interp_ratio "1"
rate "786432"
cl_updaterate "64"

// Misc
r_flush_on_pooled_ib_resize "false"
r_smooth_morph_normals "false"
sv_networkvar_validate "false"
sv_networkvar_perfieldtracking "false"
"""

# ─── COLORS ──────────────────────────────────────────────────────────────────
C_BG="#0A0A0A"; C_PANEL="#111111"; C_ACCENT="#FF3300"; C_ACCENT2="#00CCFF"
C_ACCENT3="#FFCC00"; C_TEXT="#E0E0E0"; C_TEXT_DIM="#666666"; C_TEXT_BRIGHT="#FFFFFF"
C_ENTRY_BG="#1A1A1A"; C_BORDER="#333333"; C_HOVER="#222222"; C_ON="#00FF66"
C_SIDEBAR_BG="#0D0D0D"; C_SCROLLBAR="#333333"; C_VID="#CC00FF"; C_EXEC="#00CC88"

def resource_path(rel):
    try: return os.path.join(sys._MEIPASS, rel)
    except AttributeError: return os.path.join(os.path.dirname(os.path.abspath(__file__)), rel)

def find_deadlock_path():
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
        os.path.join(home,".steam","steam","steamapps","common","Deadlock","game","citadel"),
        os.path.join(home,".local","share","Steam","steamapps","common","Deadlock","game","citadel"),
    ]
    for p in candidates:
        if os.path.isdir(p): return p
    for vdf in [r"C:\Program Files (x86)\Steam\steamapps\libraryfolders.vdf",
                r"C:\Program Files\Steam\steamapps\libraryfolders.vdf",
                os.path.join(home,".steam","steam","steamapps","libraryfolders.vdf")]:
        if not os.path.isfile(vdf): continue
        try:
            with open(vdf,"r",encoding="utf-8",errors="replace") as f:
                for line in f:
                    m = re.search(r'"path"\s+"([^"]+)"', line)
                    if m:
                        c = os.path.join(m.group(1),"steamapps","common","Deadlock","game","citadel")
                        if os.path.isdir(c): return c
        except Exception: continue
    return None

# ─── TOGGLE ───────────────────────────────────────────────────────────────────
class TDRToggle(tk.Canvas):
    def __init__(self, master, variable, **kw):
        super().__init__(master, width=44, height=20, bg=kw.pop("bg", C_PANEL),
                         highlightthickness=0, cursor="hand2", **kw)
        self.variable = variable
        self.bg_color = self["bg"]
        self._draw()
        self.bind("<Button-1>", self._toggle)
        self.variable.trace_add("write", lambda *_: self._draw())
    def _draw(self):
        self.delete("all")
        on = self.variable.get() in ("1","true","True")
        self.create_rectangle(0,4,44,18, fill=C_ON if on else "#2A2A2A", outline="")
        x = 30 if on else 2
        self.create_rectangle(x,1,x+14,21, fill=C_TEXT_BRIGHT if on else C_TEXT_DIM, outline="")
    def _toggle(self, e=None):
        v = self.variable.get()
        on = v in ("1","true","True")
        self.variable.set(("false" if on else "true") if v in ("true","false") else ("0" if on else "1"))

# ─── APP ──────────────────────────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YEWD'S OPTIMIZER")
        self.geometry("1100x720")
        self.minsize(900,600)
        self.configure(bg=C_BG)
        try: self.tk.call('tk','scaling',self.winfo_fpixels('1i')/72.0)
        except: pass
        self._set_icon()
        self.citadel_dir = None
        self.gameinfo_path = self.video_path = None
        self.gameinfo_content = self.video_content = None
        self.cvar_vars = {}
        self.active_tab = "GAMEINFO"
        self.active_category = None
        self._load_fonts()
        self._build_ui()
        self._populate_sidebar()
        self._select_category(GI_CATS[0])
        self.after(100, self._auto_load)

    def _set_icon(self):
        ico = resource_path("icon.ico"); png = resource_path("icon.png")
        try:
            if sys.platform=="win32" and os.path.isfile(ico): self.iconbitmap(ico)
            elif os.path.isfile(png):
                i = tk.PhotoImage(file=png); self.iconphoto(True,i); self._icon_ref=i
        except: pass

    def _load_fonts(self):
        fd = resource_path("fonts"); self.font_loaded = False
        try:
            if os.path.isdir(fd) and sys.platform=="win32":
                import ctypes
                for fn in os.listdir(fd): ctypes.windll.gdi32.AddFontResourceExW(os.path.join(fd,fn),0x10,0)
                self.font_loaded = True
        except: pass
        fam = "Helvetica Neue" if self.font_loaded else "Helvetica"
        avail = tkfont.families()
        if fam not in avail:
            for c in ["Helvetica Neue","Helvetica","Arial","Segoe UI"]:
                if c in avail: fam=c; break
        self.F_H=(fam,18,"bold"); self.F_SH=(fam,10,"bold"); self.F_B=(fam,9)
        self.F_BB=(fam,9,"bold"); self.F_S=(fam,8); self.F_T=(fam,7)
        self.F_C=(fam,9,"bold"); self.F_BR=(fam,24,"bold"); self.F_BS=(fam,8)
        self.F_TAB=(fam,10,"bold"); self.F_BIG=(fam,13,"bold")

    # ── UI ────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        top = tk.Frame(self, bg=C_BG, height=80); top.pack(fill="x",side="top"); top.pack_propagate(False)
        br = tk.Frame(top, bg=C_ACCENT); br.pack(side="left",fill="y")
        tk.Label(br,text="  YEWD'S OPTIMIZER  ",font=self.F_BR,bg=C_ACCENT,fg=C_TEXT_BRIGHT).pack(side="left",padx=(8,0),pady=8)
        vf=tk.Frame(br,bg=C_ACCENT); vf.pack(side="left",padx=(0,12))
        tk.Label(vf,text="DEADLOCK CONFIG",font=self.F_BS,bg=C_ACCENT,fg="#FFE0D0").pack(anchor="w")
        tk.Label(vf,text="v1.4.3",font=self.F_T,bg=C_ACCENT,fg="#FFE0D0").pack(anchor="w")
        st=tk.Canvas(top,width=30,height=80,bg=C_BG,highlightthickness=0); st.pack(side="left")
        st.create_polygon(0,0,30,0,0,80,fill=C_ACCENT,outline="")
        info=tk.Frame(top,bg=C_BG); info.pack(side="left",fill="both",expand=True,padx=16)
        self.status_label=tk.Label(info,text="DETECTING...",font=self.F_SH,bg=C_BG,fg=C_ACCENT); self.status_label.pack(anchor="w",pady=(14,2))
        self.path_label=tk.Label(info,text="",font=self.F_S,bg=C_BG,fg=C_TEXT_DIM); self.path_label.pack(anchor="w")
        self.mod_label=tk.Label(info,text="",font=self.F_T,bg=C_BG,fg=C_ACCENT2); self.mod_label.pack(anchor="w")

        btns=tk.Frame(top,bg=C_BG); btns.pack(side="right",padx=12,pady=12)
        tk.Button(btns,text="► LOCATE",font=self.F_BB,bg=C_ACCENT2,fg=C_BG,relief="flat",cursor="hand2",command=self._manual_locate,padx=10,pady=6).pack(side="left",padx=3)
        tk.Button(btns,text="↓ IMPORT",font=self.F_BB,bg="#555555",fg=C_TEXT,relief="flat",cursor="hand2",command=self._import_config,padx=10,pady=6).pack(side="left",padx=3)
        tk.Button(btns,text="↑ EXPORT",font=self.F_BB,bg="#555555",fg=C_TEXT,relief="flat",cursor="hand2",command=self._export_config,padx=10,pady=6).pack(side="left",padx=3)
        self.btn_save=tk.Button(btns,text="■ SAVE",font=self.F_BB,bg=C_ACCENT,fg=C_TEXT_BRIGHT,relief="flat",cursor="hand2",command=self._save_current,padx=10,pady=6,state="disabled")
        self.btn_save.pack(side="left",padx=3)
        tk.Button(btns,text="↺ DEFAULTS",font=self.F_BB,bg=C_BORDER,fg=C_TEXT,relief="flat",cursor="hand2",command=self._reset_defaults,padx=10,pady=6).pack(side="left",padx=3)

        tk.Frame(self,bg=C_ACCENT,height=2).pack(fill="x")
        tbar=tk.Frame(self,bg="#0E0E0E",height=32); tbar.pack(fill="x"); tbar.pack_propagate(False)
        self.tab_gi=tk.Label(tbar,text="  GAMEINFO.GI  ",font=self.F_TAB,bg=C_ACCENT,fg=C_TEXT_BRIGHT,cursor="hand2",padx=16,pady=4)
        self.tab_gi.pack(side="left"); self.tab_gi.bind("<Button-1>",lambda e:self._switch_tab("GAMEINFO"))
        self.tab_vid=tk.Label(tbar,text="  VIDEO.TXT  ",font=self.F_TAB,bg="#0E0E0E",fg=C_TEXT_DIM,cursor="hand2",padx=16,pady=4)
        self.tab_vid.pack(side="left"); self.tab_vid.bind("<Button-1>",lambda e:self._switch_tab("VIDEO"))
        self.tab_exec=tk.Label(tbar,text="  AUTOEXEC  ",font=self.F_TAB,bg="#0E0E0E",fg=C_TEXT_DIM,cursor="hand2",padx=16,pady=4)
        self.tab_exec.pack(side="left"); self.tab_exec.bind("<Button-1>",lambda e:self._switch_tab("AUTOEXEC"))
        self.vid_dot=tk.Label(tbar,text="",font=self.F_T,bg="#0E0E0E",fg=C_TEXT_DIM); self.vid_dot.pack(side="left",padx=8)
        tk.Frame(self,bg=C_BORDER,height=1).pack(fill="x")

        main=tk.Frame(self,bg=C_BG); main.pack(fill="both",expand=True)
        self.sidebar=tk.Frame(main,bg=C_SIDEBAR_BG,width=185); self.sidebar.pack(side="left",fill="y"); self.sidebar.pack_propagate(False)
        tk.Label(self.sidebar,text="CATEGORIES",font=self.F_T,bg=C_SIDEBAR_BG,fg=C_TEXT_DIM).pack(anchor="w",padx=12,pady=(12,6))
        tk.Frame(self.sidebar,bg=C_BORDER,height=1).pack(fill="x",padx=8)
        self.cat_buttons={}

        cf=tk.Frame(main,bg=C_BG); cf.pack(side="left",fill="both",expand=True)
        self.canvas=tk.Canvas(cf,bg=C_BG,highlightthickness=0)
        sb=tk.Scrollbar(cf,orient="vertical",command=self.canvas.yview,bg=C_SCROLLBAR,troughcolor=C_BG,width=8,relief="flat")
        self.canvas.configure(yscrollcommand=sb.set); sb.pack(side="right",fill="y"); self.canvas.pack(side="left",fill="both",expand=True)
        self.inner=tk.Frame(self.canvas,bg=C_BG)
        self.cwin=self.canvas.create_window((0,0),window=self.inner,anchor="nw")
        self.inner.bind("<Configure>",lambda e:self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>",lambda e:self.canvas.itemconfig(self.cwin,width=e.width))
        self.canvas.bind_all("<MouseWheel>",lambda e:self.canvas.yview_scroll(int(-1*(e.delta/120)),"units"))
        self.canvas.bind_all("<Button-4>",lambda e:self.canvas.yview_scroll(-1,"units"))
        self.canvas.bind_all("<Button-5>",lambda e:self.canvas.yview_scroll(1,"units"))

        bot=tk.Frame(self,bg=C_PANEL,height=28); bot.pack(fill="x",side="bottom"); bot.pack_propagate(False)
        self.bot_status=tk.Label(bot,text="YEWD'S OPTIMIZER v1.4.3",font=self.F_T,bg=C_PANEL,fg=C_TEXT_DIM); self.bot_status.pack(side="left",padx=12)
        self.bot_backup=tk.Label(bot,text="",font=self.F_T,bg=C_PANEL,fg=C_TEXT_DIM); self.bot_backup.pack(side="right",padx=12)

    # ── TABS ──────────────────────────────────────────────────────────────────
    def _switch_tab(self, tab):
        self.active_tab = tab
        tabs = {"GAMEINFO":(self.tab_gi,C_ACCENT), "VIDEO":(self.tab_vid,C_VID), "AUTOEXEC":(self.tab_exec,C_EXEC)}
        for t,(lbl,col) in tabs.items():
            if t==tab: lbl.configure(bg=col,fg=C_TEXT_BRIGHT)
            else: lbl.configure(bg="#0E0E0E",fg=C_TEXT_DIM)
        self._populate_sidebar()
        if tab=="AUTOEXEC":
            self._show_autoexec()
        else:
            cats = GI_CATS if tab=="GAMEINFO" else VID_CATS
            self._select_category(cats[0])

    def _populate_sidebar(self):
        for b in self.cat_buttons.values(): b.destroy()
        self.cat_buttons.clear()
        if self.active_tab=="AUTOEXEC": return  # no sidebar for autoexec
        cats,settings,ci = (GI_CATS,CONVARS,4) if self.active_tab=="GAMEINFO" else (VID_CATS,VIDEO_SETTINGS,3)
        for cat in cats:
            n=sum(1 for s in settings if s[ci]==cat)
            if n==0: continue
            label=cat.replace("VID: ","") if cat.startswith("VID: ") else cat
            btn=tk.Label(self.sidebar,text=f"  {label}  ({n})",font=self.F_C,bg=C_SIDEBAR_BG,fg=C_TEXT_DIM,anchor="w",padx=12,pady=6,cursor="hand2")
            btn.pack(fill="x")
            btn.bind("<Button-1>",lambda e,c=cat:self._select_category(c))
            btn.bind("<Enter>",lambda e,b=btn:b.configure(bg=C_HOVER) if b!=self.cat_buttons.get(self.active_category) else None)
            btn.bind("<Leave>",lambda e,b=btn:b.configure(bg=C_SIDEBAR_BG) if b!=self.cat_buttons.get(self.active_category) else None)
            self.cat_buttons[cat]=btn

    # ── CATEGORY VIEW ─────────────────────────────────────────────────────────
    def _select_category(self, category):
        accent = C_ACCENT if self.active_tab=="GAMEINFO" else C_VID
        for cat,btn in self.cat_buttons.items():
            btn.configure(bg=(accent if cat==category else C_SIDEBAR_BG), fg=(C_TEXT_BRIGHT if cat==category else C_TEXT_DIM))
        self.active_category=category
        for w in self.inner.winfo_children(): w.destroy()

        is_gi = self.active_tab=="GAMEINFO"
        settings = CONVARS if is_gi else VIDEO_SETTINGS

        label=category.replace("VID: ","") if category.startswith("VID: ") else category
        hdr=tk.Frame(self.inner,bg=C_BG); hdr.pack(fill="x",padx=20,pady=(16,4))
        tk.Label(hdr,text=f"◆ {label}",font=self.F_H,bg=C_BG,fg=C_TEXT_BRIGHT).pack(side="left")
        tk.Frame(self.inner,bg=accent,height=1).pack(fill="x",padx=20,pady=(0,12))

        for s in settings:
            if is_gi:
                name,rec,defv,desc,cat,vtype,opts = s
            else:
                name,rec,desc,cat,vtype,opts = s; defv=None
            if cat!=category: continue
            if name not in self.cvar_vars: self.cvar_vars[name]=tk.StringVar(value=rec)
            var=self.cvar_vars[name]
            row=tk.Frame(self.inner,bg=C_PANEL,padx=16,pady=10); row.pack(fill="x",padx=20,pady=2)
            left=tk.Frame(row,bg=C_PANEL); left.pack(side="left",fill="x",expand=True)
            tk.Label(left,text=name,font=self.F_BB,bg=C_PANEL,fg=C_ACCENT2).pack(anchor="w")
            tk.Label(left,text=desc,font=self.F_S,bg=C_PANEL,fg=C_TEXT_DIM).pack(anchor="w")
            tk.Label(left,text=f"DEFAULT: {defv}" if defv is not None else f"RECOMMENDED: {rec}",font=self.F_T,bg=C_PANEL,fg="#444444").pack(anchor="w")
            right=tk.Frame(row,bg=C_PANEL); right.pack(side="right",padx=(12,0))
            if vtype in ("bool","bool_str"): TDRToggle(right,var).pack(pady=4)
            elif vtype=="choice":
                ttk.Combobox(right,textvariable=var,values=opts,state="readonly",width=8,font=self.F_B).pack(pady=4)
                self._style_combo()
            elif vtype in ("int","float"):
                cf=tk.Frame(right,bg=C_PANEL); cf.pack(pady=4)
                tk.Entry(cf,textvariable=var,font=self.F_B,bg=C_ENTRY_BG,fg=C_TEXT_BRIGHT,insertbackground=C_ACCENT,relief="flat",width=8,justify="center",highlightthickness=1,highlightcolor=C_ACCENT,highlightbackground=C_BORDER).pack(side="left")
                if opts: tk.Label(cf,text=f"[{opts[0]}–{opts[1]}]",font=self.F_T,bg=C_PANEL,fg=C_TEXT_DIM).pack(side="left",padx=(6,0))
            else:
                tk.Entry(right,textvariable=var,font=self.F_B,bg=C_ENTRY_BG,fg=C_TEXT_BRIGHT,insertbackground=C_ACCENT,relief="flat",width=14,justify="center",highlightthickness=1,highlightcolor=C_ACCENT,highlightbackground=C_BORDER).pack(pady=4)
            rv=defv if defv is not None else rec
            rst=tk.Label(right,text="↺",font=(self.F_B[0],12),bg=C_PANEL,fg=C_TEXT_DIM,cursor="hand2"); rst.pack(side="right",padx=(8,0))
            rst.bind("<Button-1>",lambda e,v=var,d=rv:v.set(d))
            rst.bind("<Enter>",lambda e,l=rst:l.configure(fg=C_ACCENT))
            rst.bind("<Leave>",lambda e,l=rst:l.configure(fg=C_TEXT_DIM))
        self.canvas.yview_moveto(0)

    # ── AUTOEXEC TAB ──────────────────────────────────────────────────────────
    def _show_autoexec(self):
        self.active_category = None
        for w in self.inner.winfo_children(): w.destroy()

        cfg_dir = os.path.join(self.citadel_dir,"cfg") if self.citadel_dir else None
        autoexec_path = os.path.join(cfg_dir,"autoexec.cfg") if cfg_dir else None

        # Read current autoexec if it exists
        current = ""
        if autoexec_path and os.path.isfile(autoexec_path):
            try:
                with open(autoexec_path,"r",encoding="utf-8",errors="replace") as f: current=f.read()
            except: pass

        has_nulls = "alias +mfwd" in current
        has_optim = "zoom_sensitivity_ratio" in current and "sv_networkvar_validate" in current

        # Header
        hdr=tk.Frame(self.inner,bg=C_BG); hdr.pack(fill="x",padx=20,pady=(16,4))
        tk.Label(hdr,text="◆ AUTOEXEC.CFG",font=self.F_H,bg=C_BG,fg=C_TEXT_BRIGHT).pack(side="left")
        tk.Frame(self.inner,bg=C_EXEC,height=1).pack(fill="x",padx=20,pady=(0,12))

        # Launch options reminder
        warn=tk.Frame(self.inner,bg="#1A2A1A",padx=16,pady=12); warn.pack(fill="x",padx=20,pady=(0,12))
        tk.Label(warn,text="⚠  REQUIRED: Add  +exec autoexec.cfg  to your Steam launch options",font=self.F_BB,bg="#1A2A1A",fg=C_ACCENT3).pack(anchor="w")
        tk.Label(warn,text="Right-click Deadlock in Steam → Properties → Launch Options",font=self.F_S,bg="#1A2A1A",fg=C_TEXT_DIM).pack(anchor="w")

        # Status
        status_frame=tk.Frame(self.inner,bg=C_PANEL,padx=16,pady=10); status_frame.pack(fill="x",padx=20,pady=2)
        if autoexec_path and os.path.isfile(autoexec_path):
            tk.Label(status_frame,text=f"● autoexec.cfg found",font=self.F_BB,bg=C_PANEL,fg=C_ON).pack(anchor="w")
            tk.Label(status_frame,text=autoexec_path,font=self.F_T,bg=C_PANEL,fg=C_TEXT_DIM).pack(anchor="w")
        elif cfg_dir:
            tk.Label(status_frame,text="○ autoexec.cfg not found — will be created when you enable a config",font=self.F_BB,bg=C_PANEL,fg=C_ACCENT3).pack(anchor="w")
            tk.Label(status_frame,text=cfg_dir,font=self.F_T,bg=C_PANEL,fg=C_TEXT_DIM).pack(anchor="w")
        else:
            tk.Label(status_frame,text="✗ Deadlock install not detected — use LOCATE first",font=self.F_BB,bg=C_PANEL,fg=C_ACCENT).pack(anchor="w")
            return

        # ── Null Movement Binds ──
        null_frame=tk.Frame(self.inner,bg=C_PANEL,padx=16,pady=14); null_frame.pack(fill="x",padx=20,pady=(12,2))
        nl=tk.Frame(null_frame,bg=C_PANEL); nl.pack(side="left",fill="x",expand=True)
        tk.Label(nl,text="NULL MOVEMENT BINDS",font=self.F_BIG,bg=C_PANEL,fg=C_TEXT_BRIGHT).pack(anchor="w")
        tk.Label(nl,text="Prevents opposite keys from cancelling each other (WASD). Works in all Source games.",font=self.F_S,bg=C_PANEL,fg=C_TEXT_DIM).pack(anchor="w")
        st_null=tk.Label(nl,text="● ACTIVE" if has_nulls else "○ INACTIVE",font=self.F_T,bg=C_PANEL,fg=C_ON if has_nulls else C_TEXT_DIM)
        st_null.pack(anchor="w",pady=(4,0))

        nr=tk.Frame(null_frame,bg=C_PANEL); nr.pack(side="right")
        null_btn_text = "DISABLE" if has_nulls else "ENABLE"
        null_btn_color = C_ACCENT if has_nulls else C_ON
        tk.Button(nr,text=null_btn_text,font=self.F_BB,bg=null_btn_color,fg=C_BG,relief="flat",cursor="hand2",
                  padx=20,pady=8,command=lambda: self._toggle_autoexec_block("nulls",not has_nulls)).pack()

        # ── Optimized Config ──
        opt_frame=tk.Frame(self.inner,bg=C_PANEL,padx=16,pady=14); opt_frame.pack(fill="x",padx=20,pady=2)
        ol=tk.Frame(opt_frame,bg=C_PANEL); ol.pack(side="left",fill="x",expand=True)
        tk.Label(ol,text="OPTIMIZED AUTOEXEC",font=self.F_BIG,bg=C_PANEL,fg=C_TEXT_BRIGHT).pack(anchor="w")
        tk.Label(ol,text="Zoom sensitivity, FPS, network, graphics, and misc performance tweaks.",font=self.F_S,bg=C_PANEL,fg=C_TEXT_DIM).pack(anchor="w")
        st_opt=tk.Label(ol,text="● ACTIVE" if has_optim else "○ INACTIVE",font=self.F_T,bg=C_PANEL,fg=C_ON if has_optim else C_TEXT_DIM)
        st_opt.pack(anchor="w",pady=(4,0))

        orr=tk.Frame(opt_frame,bg=C_PANEL); orr.pack(side="right")
        opt_btn_text = "DISABLE" if has_optim else "ENABLE"
        opt_btn_color = C_ACCENT if has_optim else C_ON
        tk.Button(orr,text=opt_btn_text,font=self.F_BB,bg=opt_btn_color,fg=C_BG,relief="flat",cursor="hand2",
                  padx=20,pady=8,command=lambda: self._toggle_autoexec_block("optim",not has_optim)).pack()

        self.canvas.yview_moveto(0)

    def _toggle_autoexec_block(self, block, enable):
        """Add or remove a block from autoexec.cfg."""
        if not self.citadel_dir: return
        cfg_dir = os.path.join(self.citadel_dir,"cfg")
        os.makedirs(cfg_dir, exist_ok=True)
        autoexec_path = os.path.join(cfg_dir,"autoexec.cfg")

        current = ""
        if os.path.isfile(autoexec_path):
            try:
                with open(autoexec_path,"r",encoding="utf-8",errors="replace") as f: current=f.read()
            except: pass

        # Markers
        if block=="nulls":
            start_mark = "// ── YEWD NULL BINDS START ──"
            end_mark   = "// ── YEWD NULL BINDS END ──"
            content_block = f"{start_mark}\n{NULLS_CFG.strip()}\n{end_mark}\n"
        else:
            start_mark = "// ── YEWD OPTIMIZED CFG START ──"
            end_mark   = "// ── YEWD OPTIMIZED CFG END ──"
            content_block = f"{start_mark}\n{OPTIMIZED_CFG.strip()}\n{end_mark}\n"

        # Remove existing block if present (by markers or by content detection)
        if start_mark in current:
            pattern = re.escape(start_mark) + r".*?" + re.escape(end_mark) + r"\n?"
            current = re.sub(pattern, "", current, flags=re.DOTALL).strip()
        elif block=="nulls" and "alias +mfwd" in current:
            # Legacy removal: strip null bind lines if no markers
            lines = current.split("\n")
            null_keywords = ["alias +mfwd","alias +mback","alias +mleft","alias +mright",
                             "alias -mfwd","alias -mback","alias -mleft","alias -mright",
                             "alias checkfwd","alias checkback","alias checkleft","alias checkright",
                             "alias none","bind w +mfwd","bind s +mback","bind a +mleft","bind d +mright"]
            lines = [l for l in lines if not any(k in l for k in null_keywords)]
            current = "\n".join(lines).strip()

        if enable:
            current = current.strip() + "\n\n" + content_block

        current = current.strip() + "\n"

        try:
            with open(autoexec_path,"w",encoding="utf-8") as f: f.write(current)
            self.bot_status.configure(text=f"AUTOEXEC: {'enabled' if enable else 'disabled'} {block}")
            self._show_autoexec()  # refresh
        except PermissionError:
            messagebox.showerror("Permission Denied",f"Cannot write to:\n{autoexec_path}\n\nRun as Administrator.")
        except Exception as e:
            messagebox.showerror("Error",f"Failed to write autoexec.cfg:\n{e}")

    def _style_combo(self):
        s=ttk.Style(); s.theme_use("clam")
        s.configure("TCombobox",fieldbackground=C_ENTRY_BG,background=C_BORDER,foreground=C_TEXT_BRIGHT,arrowcolor=C_TEXT,borderwidth=0)
        s.map("TCombobox",fieldbackground=[("readonly",C_ENTRY_BG)],selectbackground=[("readonly",C_ENTRY_BG)],selectforeground=[("readonly",C_TEXT_BRIGHT)])

    # ── AUTO-LOAD ─────────────────────────────────────────────────────────────
    def _auto_load(self):
        self.citadel_dir = find_deadlock_path()
        if not self.citadel_dir:
            self.status_label.configure(text="AUTO-DETECT FAILED",fg=C_ACCENT3)
            self.path_label.configure(text="Use LOCATE to find your citadel folder",fg=C_TEXT_DIM)
            return
        self._load_from_dir(self.citadel_dir)

    def _manual_locate(self):
        d=filedialog.askdirectory(title="Select Deadlock citadel folder")
        if not d: return
        self.citadel_dir=d; self._load_from_dir(d)

    def _load_from_dir(self, d):
        self.status_label.configure(text="INSTALL FOUND",fg=C_ON)
        self.path_label.configure(text=d,fg=C_TEXT)
        bk=[]
        gi=os.path.join(d,"gameinfo.gi")
        if os.path.isfile(gi): self._load_file(gi,"gameinfo"); bk.append("gameinfo.gi")
        vt=os.path.join(d,"cfg","video.txt")
        if os.path.isfile(vt):
            self._load_file(vt,"video"); bk.append("video.txt")
            self.vid_dot.configure(text="● video.txt loaded",fg=C_ON)
        else: self.vid_dot.configure(text="○ video.txt not found",fg=C_ACCENT3)
        if bk: self.bot_backup.configure(text="BACKUPS: "+", ".join(f"{b}.backup_original" for b in bk))
        self.btn_save.configure(state="normal")
        if self.active_category: self._select_category(self.active_category)

    def _load_file(self, path, kind):
        try:
            with open(path,"r",encoding="utf-8",errors="replace") as f: content=f.read()
        except Exception as e: messagebox.showerror("Error",f"Failed to read {path}:\n{e}"); return
        backup=path+".backup_original"
        if not os.path.exists(backup):
            try: shutil.copy2(path,backup)
            except: pass
        if kind=="gameinfo": self.gameinfo_path=path; self.gameinfo_content=content; self._parse_gameinfo(content)
        else: self.video_path=path; self.video_content=content; self._parse_video(content)

    # ── PARSING ───────────────────────────────────────────────────────────────
    def _parse_gameinfo(self, content):
        for cvar in CONVARS:
            name=cvar[0]
            for line in content.split("\n"):
                s=line.strip()
                if s.startswith("//"): continue
                m=re.match(rf'^\s*{re.escape(name)}\s+"([^"]*)"',s) or re.match(rf'^\s*{re.escape(name)}\s+(\S+)',s)
                if m:
                    v=m.group(1).strip()
                    if name in self.cvar_vars: self.cvar_vars[name].set(v)
                    else: self.cvar_vars[name]=tk.StringVar(value=v)
                    break

    def _parse_video(self, content):
        for vs in VIDEO_SETTINGS:
            name=vs[0]
            for line in content.split("\n"):
                s=line.strip()
                if s.startswith("//"): continue
                m=re.match(rf'^\s*"{re.escape(name)}"\s+"([^"]*)"',s)
                if m:
                    v=m.group(1).strip()
                    if name in self.cvar_vars: self.cvar_vars[name].set(v)
                    else: self.cvar_vars[name]=tk.StringVar(value=v)
                    break

    # ── IMPORT / EXPORT ───────────────────────────────────────────────────────
    def _export_config(self):
        """Export current tab's file as a native copy."""
        if self.active_tab=="GAMEINFO":
            if not self.gameinfo_path or not self.gameinfo_content:
                messagebox.showerror("Error","No gameinfo.gi loaded to export."); return
            # Build the updated content first (same logic as save)
            content = self._build_gameinfo_content()
            path = filedialog.asksaveasfilename(title="Export gameinfo.gi", defaultextension=".gi",
                                                filetypes=[("GameInfo","*.gi"),("All Files","*.*")],
                                                initialfile="gameinfo.gi")
            if not path: return
            try:
                with open(path,"w",encoding="utf-8") as f: f.write(content)
                self.bot_status.configure(text=f"EXPORTED: {os.path.basename(path)}")
            except Exception as e: messagebox.showerror("Error",f"Export failed:\n{e}")
        elif self.active_tab=="VIDEO":
            if not self.video_path or not self.video_content:
                messagebox.showerror("Error","No video.txt loaded to export."); return
            content = self._build_video_content()
            path = filedialog.asksaveasfilename(title="Export video.txt", defaultextension=".txt",
                                                filetypes=[("Text","*.txt"),("All Files","*.*")],
                                                initialfile="video.txt")
            if not path: return
            try:
                with open(path,"w",encoding="utf-8") as f: f.write(content)
                self.bot_status.configure(text=f"EXPORTED: {os.path.basename(path)}")
            except Exception as e: messagebox.showerror("Error",f"Export failed:\n{e}")
        else:
            messagebox.showinfo("Export","Autoexec configs are managed directly — nothing to export.")

    def _import_config(self):
        """Import a gameinfo.gi or video.txt file, parse it, and prepare to save as the correct filename."""
        if self.active_tab=="GAMEINFO":
            path = filedialog.askopenfilename(title="Import gameinfo.gi",
                                              filetypes=[("GameInfo","*.gi"),("All Files","*.*")])
            if not path: return
            try:
                with open(path,"r",encoding="utf-8",errors="replace") as f: content=f.read()
            except Exception as e: messagebox.showerror("Error",f"Import failed:\n{e}"); return
            # If we have a citadel dir, set the target path to the correct gameinfo.gi
            if self.citadel_dir:
                self.gameinfo_path = os.path.join(self.citadel_dir,"gameinfo.gi")
            self.gameinfo_content = content
            self._parse_gameinfo(content)
            self.bot_status.configure(text=f"IMPORTED: {os.path.basename(path)} → will save as gameinfo.gi")
            if self.active_category: self._select_category(self.active_category)
        elif self.active_tab=="VIDEO":
            path = filedialog.askopenfilename(title="Import video.txt",
                                              filetypes=[("Text","*.txt"),("Config","*.cfg"),("All Files","*.*")])
            if not path: return
            try:
                with open(path,"r",encoding="utf-8",errors="replace") as f: content=f.read()
            except Exception as e: messagebox.showerror("Error",f"Import failed:\n{e}"); return
            if self.citadel_dir:
                self.video_path = os.path.join(self.citadel_dir,"cfg","video.txt")
            self.video_content = content
            self._parse_video(content)
            self.bot_status.configure(text=f"IMPORTED: {os.path.basename(path)} → will save as video.txt")
            if self.active_category: self._select_category(self.active_category)
        else:
            messagebox.showinfo("Import","Autoexec configs are managed directly — nothing to import.")

    # ── CONTENT BUILDERS ────────────────────────────────────────────────────────
    def _build_gameinfo_content(self):
        """Build updated gameinfo.gi content string from current cvar values."""
        lines=self.gameinfo_content.split("\n"); out=[]
        for line in lines:
            s=line.strip()
            if s.startswith("//"): out.append(line); continue
            done=False
            for cvar in CONVARS:
                name=cvar[0]
                if name not in self.cvar_vars: continue
                m=re.match(rf'^(\s*){re.escape(name)}(\s+)"([^"]*)"(.*)',s)
                if not m: m=re.match(rf'^(\s*){re.escape(name)}(\s+)(\S+)(.*)',s)
                if m:
                    nv=self.cvar_vars[name].get(); sp,ov,rest=m.group(2),m.group(3),m.group(4)
                    ws=""
                    for ch in line:
                        if ch in (" ","\t"): ws+=ch
                        else: break
                    vs=f'"{nv}"' if ('"'+ov+'"') in s else nv
                    out.append(f"{ws}{name}{sp}{vs}{rest}"); done=True; break
            if not done: out.append(line)
        return "\n".join(out)

    def _build_video_content(self):
        """Build updated video.txt content string from current setting values."""
        lines=self.video_content.split("\n"); out=[]
        for line in lines:
            s=line.strip()
            if s.startswith("//"): out.append(line); continue
            done=False
            for vs in VIDEO_SETTINGS:
                name=vs[0]
                if name not in self.cvar_vars: continue
                m=re.match(rf'^(\s*)"{re.escape(name)}"(\s+)"([^"]*)"(.*)',s)
                if m:
                    nv=self.cvar_vars[name].get(); sp,rest=m.group(2),m.group(4)
                    ws=""
                    for ch in line:
                        if ch in (" ","\t"): ws+=ch
                        else: break
                    out.append(f'{ws}"{name}"{sp}"{nv}"{rest}'); done=True; break
            if not done: out.append(line)
        return "\n".join(out)

    # ── SAVE ──────────────────────────────────────────────────────────────────
    def _save_current(self):
        saved=[]
        if self.gameinfo_path and self.gameinfo_content:
            if self._save_gameinfo(): saved.append("gameinfo.gi")
        if self.video_path and self.video_content:
            if self._save_video(): saved.append("video.txt")
        if saved:
            self.status_label.configure(text="SAVED",fg=C_ON)
            self.bot_status.configure(text=f"SAVED: {', '.join(saved)}")
        elif self.active_tab!="AUTOEXEC":
            messagebox.showerror("Error","No files loaded to save.")

    def _save_gameinfo(self):
        content = self._build_gameinfo_content()
        try:
            with open(self.gameinfo_path,"w",encoding="utf-8") as f: f.write(content)
            self.gameinfo_content=content; return True
        except PermissionError: messagebox.showerror("Permission Denied",f"Cannot write to:\n{self.gameinfo_path}\n\nRun as Administrator.")
        except Exception as e: messagebox.showerror("Error",f"gameinfo.gi save failed:\n{e}")
        return False

    def _save_video(self):
        content = self._build_video_content()
        try:
            with open(self.video_path,"w",encoding="utf-8") as f: f.write(content)
            self.video_content=content; return True
        except PermissionError: messagebox.showerror("Permission Denied",f"Cannot write to:\n{self.video_path}\n\nRun as Administrator.")
        except Exception as e: messagebox.showerror("Error",f"video.txt save failed:\n{e}")
        return False

    # ── RESET ─────────────────────────────────────────────────────────────────
    def _reset_defaults(self):
        if self.active_tab=="GAMEINFO":
            if not messagebox.askyesno("Reset","Reset ALL gameinfo values to OptimizationLock defaults?"): return
            for c in CONVARS:
                if c[0] in self.cvar_vars: self.cvar_vars[c[0]].set(c[1])
        elif self.active_tab=="VIDEO":
            if not messagebox.askyesno("Reset","Reset ALL video values to recommended defaults?\n(VendorID/DeviceID unchanged)"): return
            for v in VIDEO_SETTINGS:
                if v[0] in ("VendorID","DeviceID"): continue
                if v[0] in self.cvar_vars and v[1]: self.cvar_vars[v[0]].set(v[1])
        else: return
        self.mod_label.configure(text="ALL VALUES RESET")
        if self.active_category: self._select_category(self.active_category)

if __name__=="__main__":
    App().mainloop()
