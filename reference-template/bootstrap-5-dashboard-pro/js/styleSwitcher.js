"use strict";

function buildColorSwatchesHtml(inputPrefix, radioName, includeWhiteSwatch) {
  var indices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15];
  var htmlParts = [];
  for (var i = 0; i < indices.length; i++) {
    var num = indices[i];
    if (num === 8 && !includeWhiteSwatch) continue;
    var inputId = inputPrefix + "_color_" + num;
    var extraClass = num === 1 ? ' class="bg-label-pattern"' : (num === 8 ? ' class="border"' : '');
    htmlParts.push(
      '<span>' +
        '<input class="chk-col-primary filled-in" id="' + inputId + '" name="' + radioName + '" type="radio" value="color_' + num + '">' +
        '<label for="' + inputId + '"' + extraClass + ' title="Color ' + num + '"></label>' +
      '</span>'
    );
  }
  return htmlParts.join(' ');
}

function addSwitcher() {
  if (jQuery('#dlabSwitcher').length > 0 || jQuery('.sidebar-right').length > 0) {
    return;
  }

  var dlabSwitcher =
    '<div class="sidebar-right" id="dlabSwitcher">' +
      '<div class="bg-overlay"></div>' +
      '<a class="sidebar-right-trigger wave-effect wave-effect-x" title="UI Kit Settings" href="javascript:void(0);" aria-label="Open UI Kit Settings">' +
        '<span><i class="fa fa-cog fa-spin" aria-hidden="true"></i></span>' +
      '</a>' +
      '<a class="sidebar-close-trigger" href="javascript:void(0);" aria-label="Close UI Kit Settings">' +
        '<span><i class="la-times las" aria-hidden="true"></i></span>' +
      '</a>' +
      '<div class="sidebar-right-inner">' +
        '<h4>Appearance Settings <button type="button" onclick="deleteAllCookie()" class="btn btn-primary btn-sm float-end">Reset</button></h4>' +
        '<div class="card-tabs">' +
          '<ul class="nav nav-tabs" role="tablist">' +
            '<li class="nav-item"><a class="nav-link active" href="#uiKitTabTheme" data-bs-toggle="tab">Colors</a></li>' +
            '<li class="nav-item"><a class="nav-link" href="#uiKitTabHeader" data-bs-toggle="tab">Menu</a></li>' +
            '<li class="nav-item"><a class="nav-link" href="#uiKitTabContent" data-bs-toggle="tab">Page &amp; Font</a></li>' +
          '</ul>' +
        '</div>' +
        '<div class="tab-content tab-content-default tabcontent-border">' +
          '<div class="fade tab-pane active show" id="uiKitTabTheme">' +
            '<div class="admin-settings">' +
              '<div class="row">' +
                '<div class="col-sm-12">' +
                  '<p>Screen Mode</p>' +
                  '<select class="default-select wide form-control" id="theme_version" name="theme_version">' +
                    '<option value="light">Light</option>' +
                    '<option value="dark">Dark</option>' +
                  '</select>' +
                '</div>' +
                '<div class="col-sm-6">' +
                  '<p>Main Color</p>' +
                  '<div>' + buildColorSwatchesHtml('primary', 'primary_bg', false) + '</div>' +
                '</div>' +
                '<div class="col-sm-6">' +
                  '<p>Top Logo Box</p>' +
                  '<div>' + buildColorSwatchesHtml('nav_header', 'navigation_header', true) + '</div>' +
                '</div>' +
                '<div class="col-sm-6">' +
                  '<p>Top Bar Color</p>' +
                  '<div>' + buildColorSwatchesHtml('header', 'header_bg', true) + '</div>' +
                '</div>' +
                '<div class="col-sm-6">' +
                  '<p>Sidebar Color</p>' +
                  '<div>' + buildColorSwatchesHtml('sidebar', 'sidebar_bg', true) + '</div>' +
                '</div>' +
              '</div>' +
            '</div>' +
          '</div>' +
          '<div class="fade tab-pane" id="uiKitTabHeader">' +
            '<div class="admin-settings">' +
              '<div class="row">' +
                '<div class="col-sm-6">' +
                  '<p>Menu Layout</p>' +
                  '<select class="default-select wide form-control" id="theme_layout" name="theme_layout">' +
                    '<option value="vertical">Side Menu</option>' +
                    '<option value="horizontal">Top Menu</option>' +
                  '</select>' +
                '</div>' +
                '<div class="col-sm-6">' +
                  '<p>Top Bar Position</p>' +
                  '<select class="default-select wide form-control" id="header_position" name="header_position">' +
                    '<option value="fixed">Pinned</option>' +
                    '<option value="static">Scrolls</option>' +
                  '</select>' +
                '</div>' +
                '<div class="col-sm-6">' +
                  '<p>Sidebar Size</p>' +
                  '<select class="default-select wide form-control" id="sidebar_style" name="sidebar_style">' +
                    '<option value="full">Full</option>' +
                    '<option value="mini">Mini Icons</option>' +
                    '<option value="compact">Compact</option>' +
                    '<option value="modern">Modern</option>' +
                    '<option value="overlay">Slide Over</option>' +
                    '<option value="icon-hover">Expand on Hover</option>' +
                  '</select>' +
                '</div>' +
                '<div class="col-sm-6">' +
                  '<p>Sidebar Position</p>' +
                  '<select class="default-select wide form-control" id="sidebar_position" name="sidebar_position">' +
                    '<option value="fixed">Pinned</option>' +
                    '<option value="static">Scrolls</option>' +
                  '</select>' +
                '</div>' +
              '</div>' +
            '</div>' +
          '</div>' +
          '<div class="fade tab-pane" id="uiKitTabContent">' +
            '<div class="admin-settings">' +
              '<div class="row">' +
                '<div class="col-sm-6">' +
                  '<p>Page Width</p>' +
                  '<select class="default-select wide form-control" id="container_layout" name="container_layout">' +
                    '<option value="wide">Full Width</option>' +
                    '<option value="boxed">Centered Box</option>' +
                    '<option value="wide-boxed">Wide Box</option>' +
                  '</select>' +
                '</div>' +
                '<div class="col-sm-6">' +
                  '<p>Font</p>' +
                  '<select class="default-select wide form-control" id="typography" name="typography">' +
                    '<option value="cairo">Cairo</option>' +
                    '<option value="roboto">Roboto</option>' +
                    '<option value="poppins">Poppins</option>' +
                    '<option value="opensans">Open Sans</option>' +
                    '<option value="HelveticaNeue">Helvetica Neue</option>' +
                  '</select>' +
                '</div>' +
              '</div>' +
            '</div>' +
          '</div>' +
        '</div>' +
      '</div>' +
    '</div>';

  var presets = [
    { id: 0, title: 'Default Light Teal', badge: '#5bcfc5', sidebar: '#ffffff', bg: '#f6f6f6' },
    { id: 1, title: 'Teal Sidebar Full', badge: '#5bcfc5', sidebar: '#5bcfc5', bg: '#f6f6f6' },
    { id: 2, title: 'Deep Purple Compact', badge: '#4d06a5', sidebar: '#4d06a5', bg: '#f6f6f6' },
    { id: 3, title: 'Amber Gold Full', badge: '#ffc107', sidebar: '#ffc107', bg: '#f6f6f6' },
    { id: 4, title: 'Dark Obsidian Teal', badge: '#5bcfc5', sidebar: '#212130', bg: '#171622' },
    { id: 5, title: 'Crimson Horizontal', badge: '#dc3545', sidebar: '#dc3545', bg: '#f6f6f6' },
    { id: 6, title: 'Cyan Mini Rail', badge: '#17a2b8', sidebar: '#17a2b8', bg: '#f6f6f6' },
    { id: 7, title: 'Warm Orange Compact', badge: '#fd7e14', sidebar: '#ffffff', bg: '#f6f6f6' },
    { id: 8, title: 'Forest Icon-Hover', badge: '#4cb32b', sidebar: '#4cb32b', bg: '#f6f6f6' }
  ];

  var presetCardsHtml = '';
  for (var p = 0; p < presets.length; p++) {
    var pr = presets[p];
    presetCardsHtml +=
      '<div class="p-3 mb-2 rounded border d-flex align-items-center justify-content-between" style="background:' + pr.bg + ';">' +
        '<div class="d-flex align-items-center">' +
          '<span class="d-inline-block rounded me-2 border" style="width:24px;height:24px;background:' + pr.sidebar + ';"></span>' +
          '<span class="d-inline-block rounded me-2" style="width:24px;height:24px;background:' + pr.badge + ';"></span>' +
          '<strong style="color:' + (pr.bg === '#171622' ? '#ffffff' : '#000000') + ';font-size:13px;">' + pr.title + '</strong>' +
        '</div>' +
        '<button type="button" data-theme="' + pr.id + '" class="btn dlab_theme_demo btn-primary btn-xs">Apply</button>' +
      '</div>';
  }

  var demoPanel =
    '<div class="dlab-demo-panel">' +
      '<div class="bg-close"></div>' +
      '<a class="dlab-demo-trigger" title="Theme Presets" href="javascript:void(0);" aria-label="Open Theme Presets">' +
        '<span><i class="las la-swatchbook" aria-hidden="true"></i></span>' +
      '</a>' +
      '<div class="dlab-demo-inner">' +
        '<div class="dlab-demo-header d-flex justify-content-between align-items-center mb-3">' +
          '<h4 class="mb-0">Quick Theme Presets</h4>' +
          '<a class="dlab-demo-close" href="javascript:void(0);" aria-label="Close Presets"><span><i class="las la-times" aria-hidden="true"></i></span></a>' +
        '</div>' +
        '<div class="dlab-demo-content" style="max-height:calc(100vh - 140px);overflow-y:auto;">' +
          presetCardsHtml +
          '<button type="button" class="btn btn-outline-primary btn-sm w-100 mt-2" onclick="deleteAllCookie()">Reset All Settings</button>' +
        '</div>' +
      '</div>' +
    '</div>';

  jQuery('body').append(dlabSwitcher + demoPanel);

  if (jQuery.fn.niceSelect) {
    jQuery('.sidebar-right select.default-select').niceSelect();
  }

  jQuery('.sidebar-right-trigger').on('click', function () {
    jQuery('.sidebar-right').toggleClass('show');
  });
  jQuery('.sidebar-close-trigger, .sidebar-right .bg-overlay').on('click', function () {
    jQuery('.sidebar-right').removeClass('show');
  });
  jQuery('.dlab-demo-trigger').on('click', function () {
    jQuery('.dlab-demo-panel').toggleClass('show');
  });
  jQuery('.dlab-demo-close, .dlab-demo-panel .bg-close').on('click', function () {
    jQuery('.dlab-demo-panel').removeClass('show');
  });
}

(function ($) {
  "use strict";
  addSwitcher();

  var body = $('body');
  var html = $('html');

  $('#typography').on('change', function () {
    body.attr('data-typography', this.value);
    setCookie('typography', this.value);
  });

  $('#theme_version').on('change', function () {
    body.attr('data-theme-version', this.value);
    html.attr('data-theme-version', this.value);
    setCookie('version', this.value);
    try {
      localStorage.setItem('clipstudio_theme', this.value);
    } catch (e) {}
  });

  $('#sidebar_position').on('change', function () {
    if (this.value === "fixed" && body.attr('data-sidebar-style') === "modern" && body.attr('data-layout') === "vertical") {
      alert("Modern sidebar layout requires Static sidebar position.");
      return;
    }
    body.attr('data-sidebar-position', this.value);
    setCookie('sidebarPosition', this.value);
  });

  $('#header_position').on('change', function () {
    body.attr('data-header-position', this.value);
    setCookie('headerPosition', this.value);
  });

  $('#theme_layout').on('change', function () {
    if (body.attr('data-sidebar-style') === 'overlay') {
      body.attr('data-sidebar-style', 'full');
    }
    body.attr('data-layout', this.value);
    setCookie('layout', this.value);
  });

  $('#container_layout').on('change', function () {
    if (this.value === "boxed" && body.attr('data-layout') === "vertical" && body.attr('data-sidebar-style') === "full") {
      body.attr('data-sidebar-style', 'overlay');
    }
    body.attr('data-container', this.value);
    setCookie('containerLayout', this.value);
  });

  $('#sidebar_style').on('change', function () {
    if (body.attr('data-layout') === "horizontal" && this.value === "overlay") {
      alert("Overlay style is not supported in Horizontal layout.");
      return;
    }
    if (body.attr('data-layout') === "vertical" && body.attr('data-container') === "boxed" && this.value === "full") {
      alert("Full sidebar style is not supported in Vertical Boxed layout.");
      return;
    }
    if (body.attr('data-layout') === "vertical" && this.value === "modern" && body.attr('data-sidebar-position') === "fixed") {
      alert("Switch Sidebar Position to Static before selecting Modern sidebar.");
      return;
    }
    body.attr('data-sidebar-style', this.value);
    if (this.value === 'icon-hover') {
      $('.dlabnav').on('mouseenter', function () {
        $('#main-wrapper').addClass('iconhover-toggle');
      }).on('mouseleave', function () {
        $('#main-wrapper').removeClass('iconhover-toggle');
      });
    }
    setCookie('sidebarStyle', this.value);
  });

  $('input[name="navigation_header"]').on('click', function () {
    body.attr('data-nav-headerbg', this.value);
    setCookie('navheaderBg', this.value);
  });

  $('input[name="header_bg"]').on('click', function () {
    body.attr('data-headerbg', this.value);
    setCookie('headerBg', this.value);
  });

  $('input[name="sidebar_bg"]').on('click', function () {
    body.attr('data-sibebarbg', this.value);
    setCookie('sidebarBg', this.value);
  });

  $('input[name="primary_bg"]').on('click', function () {
    body.attr('data-primary', this.value);
    setCookie('primary', this.value);
  });

})(jQuery);
