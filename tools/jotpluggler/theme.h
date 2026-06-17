#pragma once

#include "imgui.h"

#include <array>
#include <cstdint>

// Color primitives. Kept at global scope so the many dynamic call sites
// (`color_rgb(r, g, b)`, `color_rgb(triple, alpha)`) stay unqualified.

// 0-255 RGB (+ 0-1 alpha) -> ImVec4, for ImGui/ImPlot style and the *Colored APIs.
inline ImVec4 color_rgb(int r, int g, int b, float alpha = 1.0f) {
  return ImVec4(static_cast<float>(r) / 255.0f,
                static_cast<float>(g) / 255.0f,
                static_cast<float>(b) / 255.0f,
                alpha);
}

inline ImVec4 color_rgb(const std::array<uint8_t, 3> &color, float alpha = 1.0f) {
  return color_rgb(color[0], color[1], color[2], alpha);
}

// 0-255 RGB (+ 0-255 alpha) -> packed ImU32, for ImDrawList. Matches IM_COL32.
constexpr ImU32 color_u32(const std::array<uint8_t, 3> &c, int alpha = 255) {
  return IM_COL32(c[0], c[1], c[2], alpha);
}

// The jotpluggler color vocabulary. Every color is an 0-255 RGB triple; build an
// ImVec4 with color_rgb(theme::name[, alpha]) or an ImU32 with color_u32(...).
namespace theme {

using Rgb = std::array<uint8_t, 3>;

// Text
inline constexpr Rgb ink           = {74, 80, 88};     // primary body text
inline constexpr Rgb icon_strong   = {72, 79, 88};     // active icons / glyphs
inline constexpr Rgb heading       = {57, 62, 69};     // titles, headings, legend text
inline constexpr Rgb text_muted    = {116, 124, 133};  // secondary text
inline constexpr Rgb text_subtle   = {96, 104, 113};   // expanded log body
inline constexpr Rgb text_faint    = {138, 146, 156};  // idle glyphs
inline constexpr Rgb axis_text      = {95, 103, 112};  // plot axis / inlay text
inline constexpr Rgb crosshair      = {120, 128, 138}; // plot crosshair / scrub readout
inline constexpr Rgb text_disabled  = {108, 118, 128}; // disabled text / plot cursor line
inline constexpr Rgb sidebar_label  = {102, 110, 118}; // sidebar section labels
inline constexpr Rgb placeholder    = {187, 187, 187}; // frame-not-ready text

// Status & accents
inline constexpr Rgb engaged    = {0, 163, 108};
inline constexpr Rgb alert_info = {255, 195, 0};
inline constexpr Rgb alert_crit = {199, 0, 57};
inline constexpr Rgb neutral    = {111, 143, 175};  // "none" timeline / state
inline constexpr Rgb accent     = {60, 111, 202};   // selection blue
inline constexpr Rgb live       = {38, 135, 67};    // stream status: live
inline constexpr Rgb paused     = {168, 119, 34};   // stream status: paused
inline constexpr Rgb error      = {155, 63, 63};    // stream status: error
inline constexpr Rgb ok         = {58, 126, 73};    // form ready / valid
inline constexpr Rgb warn       = {180, 122, 44};   // form not-ready
inline constexpr Rgb invalid    = {200, 72, 64};    // form error

// Log levels
inline constexpr Rgb log_active    = {46, 54, 63};
inline constexpr Rgb log_alert     = {50, 100, 200};
inline constexpr Rgb log_critical  = {176, 26, 18};
inline constexpr Rgb log_error     = {200, 50, 40};
inline constexpr Rgb log_warning   = {200, 130, 0};
inline constexpr Rgb log_info      = {80, 86, 94};
inline constexpr Rgb log_default   = {126, 133, 141};
inline constexpr Rgb log_highlight = {80, 140, 210};  // active-row tint

// Surfaces
inline constexpr Rgb white          = {255, 255, 255};
inline constexpr Rgb window_bg      = {250, 250, 251};
inline constexpr Rgb titlebar_bg    = {252, 252, 253};
inline constexpr Rgb popup_bg       = {248, 249, 251};  // popups, fps overlay, legend
inline constexpr Rgb pane_bg        = {238, 240, 244};
inline constexpr Rgb dialog_bg      = {244, 246, 248};
inline constexpr Rgb sidebar_bg     = {247, 248, 250};
inline constexpr Rgb chip_bg        = {247, 249, 252};
inline constexpr Rgb info_chip_bg   = {239, 243, 248};
inline constexpr Rgb info_chip_hi   = {220, 229, 240};
inline constexpr Rgb row_hover      = {225, 231, 239};
inline constexpr Rgb tab_idle       = {210, 217, 225};
inline constexpr Rgb tab_hovered    = {224, 230, 237};
inline constexpr Rgb tab_selected   = {242, 245, 248};
inline constexpr Rgb selection      = {252, 211, 77};   // plot box-select
inline constexpr Rgb axis_bg_hi     = {214, 220, 228};
inline constexpr Rgb axis_bg_active = {199, 209, 222};
inline constexpr Rgb axis_grid      = {188, 196, 206};
inline constexpr Rgb grid_line      = {210, 214, 220};  // state-block separators
inline constexpr Rgb placeholder_bg = {45, 47, 50};     // frame-not-ready box

// Borders & lines
inline constexpr Rgb border             = {186, 190, 196};  // plot / pane frame
inline constexpr Rgb border_strong      = {194, 198, 204};  // window / separator
inline constexpr Rgb popup_border       = {190, 197, 205};
inline constexpr Rgb dialog_border      = {186, 191, 198};
inline constexpr Rgb sidebar_border     = {188, 193, 199};
inline constexpr Rgb legend_border      = {168, 175, 184};
inline constexpr Rgb chip_border        = {184, 191, 200};
inline constexpr Rgb chip_separator     = {162, 170, 178};
inline constexpr Rgb fps_border         = {182, 188, 196};
inline constexpr Rgb placeholder_border = {95, 100, 106};
inline constexpr Rgb timeline_axis      = {60, 70, 80};     // sidebar viewport edges
inline constexpr Rgb timeline_border    = {170, 178, 186};
inline constexpr Rgb timeline_cursor    = {220, 60, 50};
inline constexpr Rgb camera_border      = {184, 189, 196};
inline constexpr Rgb camera_box         = {112, 120, 129};

// Accent fills
inline constexpr Rgb docking_preview = {69, 115, 184};
inline constexpr Rgb drop_zone_fill   = {70, 130, 220};
inline constexpr Rgb drop_zone_border = {45, 95, 175};
inline constexpr Rgb feedback_bg      = {46, 125, 80};
inline constexpr Rgb feedback_border  = {35, 96, 61};
inline constexpr Rgb feedback_text    = {247, 251, 248};

// Map
inline constexpr Rgb map_bg            = {244, 243, 238};
inline constexpr Rgb map_water_fill    = {193, 216, 235};
inline constexpr Rgb map_water_outline = {143, 173, 201};
inline constexpr Rgb map_water_line    = {156, 186, 214};
inline constexpr Rgb map_route_halo    = {31, 40, 50};
inline constexpr Rgb map_place_label   = {84, 93, 105};
inline constexpr Rgb map_node_label    = {110, 118, 128};

// Curve auto-assignment palette (a pane's curves cycle through these).
inline constexpr std::array<Rgb, 10> curve_palette = {{
  {35, 107, 180}, {220, 82, 52}, {67, 160, 71}, {243, 156, 18}, {123, 97, 255},
  {0, 150, 136}, {214, 48, 49}, {52, 73, 94}, {197, 90, 17}, {96, 125, 139},
}};

// Discrete state-block fill palette.
inline constexpr std::array<Rgb, 8> state_palette = {{
  {111, 143, 175}, {0, 163, 108}, {255, 195, 0}, {199, 0, 57},
  {123, 97, 255}, {0, 150, 136}, {214, 48, 49}, {52, 73, 94},
}};

// Route-id chip part colors: dongle, log id, slice, selector.
inline constexpr std::array<std::array<int, 3>, 4> route_chip_palette = {{
  {70, 96, 126}, {100, 86, 148}, {72, 112, 86}, {156, 104, 38},
}};

// Global ImGui style colors, applied once at startup (see configure_style).
struct ColorDef { ImGuiCol idx; int r, g, b; };
inline constexpr ColorDef imgui_colors[] = {
  {ImGuiCol_WindowBg, 250, 250, 251},  {ImGuiCol_ChildBg, 255, 255, 255},
  {ImGuiCol_Border, 194, 198, 204},    {ImGuiCol_TitleBg, 252, 252, 253},
  {ImGuiCol_TitleBgActive, 252, 252, 253}, {ImGuiCol_TitleBgCollapsed, 252, 252, 253},
  {ImGuiCol_Text, 74, 80, 88},         {ImGuiCol_TextDisabled, 108, 118, 128},
  {ImGuiCol_Button, 255, 255, 255},    {ImGuiCol_ButtonHovered, 246, 248, 250},
  {ImGuiCol_ButtonActive, 238, 240, 244}, {ImGuiCol_FrameBg, 255, 255, 255},
  {ImGuiCol_FrameBgHovered, 248, 249, 251}, {ImGuiCol_FrameBgActive, 241, 244, 248},
  {ImGuiCol_Header, 243, 245, 248},    {ImGuiCol_HeaderHovered, 237, 240, 244},
  {ImGuiCol_HeaderActive, 232, 236, 240}, {ImGuiCol_PopupBg, 248, 249, 251},
  {ImGuiCol_MenuBarBg, 232, 236, 241}, {ImGuiCol_Separator, 194, 198, 204},
  {ImGuiCol_ScrollbarBg, 240, 242, 245}, {ImGuiCol_ScrollbarGrab, 202, 207, 214},
  {ImGuiCol_ScrollbarGrabHovered, 180, 186, 194}, {ImGuiCol_ScrollbarGrabActive, 164, 171, 180},
  {ImGuiCol_Tab, 219, 224, 230},       {ImGuiCol_TabHovered, 232, 236, 241},
  {ImGuiCol_TabSelected, 250, 251, 253}, {ImGuiCol_TabSelectedOverline, 92, 109, 136},
  {ImGuiCol_TabDimmed, 213, 219, 226}, {ImGuiCol_TabDimmedSelected, 244, 247, 249},
  {ImGuiCol_TabDimmedSelectedOverline, 92, 109, 136}, {ImGuiCol_DockingEmptyBg, 244, 246, 248},
};

}  // namespace theme
