"use strict";

var themeOptionArr = {
  typography: '',
  version: '',
  layout: '',
  primary: '',
  headerBg: '',
  navheaderBg: '',
  sidebarBg: '',
  sidebarStyle: '',
  sidebarPosition: '',
  headerPosition: '',
  containerLayout: ''
};

/* Persistent 365-Day Cookie Helpers */
function setCookie(cname, cvalue) {
  var d = new Date();
  d.setTime(d.getTime() + (365 * 24 * 60 * 60 * 1000));
  var expires = "expires=" + d.toUTCString();
  document.cookie = cname + "=" + encodeURIComponent(cvalue) + ";" + expires + ";path=/;SameSite=Lax";
}

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie || '');
  var ca = decodedCookie.split(';');
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i].trim();
    if (c.indexOf(name) === 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function deleteCookie(cname) {
  document.cookie = cname + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
}

function deleteAllCookie(reload) {
  if (reload === undefined) reload = true;
  jQuery.each(themeOptionArr, function (optionKey) {
    deleteCookie(optionKey);
  });
  try {
    localStorage.removeItem('clipstudio_theme');
  } catch (e) {}
  if (reload) {
    location.reload();
  }
}

(function ($) {
  "use strict";

  var theme = (typeof getUrlParams === 'function') ? getUrlParams('theme') : undefined;

  var dezThemePresets = {
    0: {
      typography: "cairo",
      version: "light",
      layout: "vertical",
      primary: "color_1",
      headerBg: "color_1",
      navheaderBg: "color_1",
      sidebarBg: "color_1",
      sidebarStyle: "full",
      sidebarPosition: "fixed",
      headerPosition: "fixed",
      containerLayout: "wide"
    },
    1: {
      typography: "cairo",
      version: "light",
      layout: "vertical",
      primary: "color_1",
      headerBg: "color_1",
      navheaderBg: "color_3",
      sidebarBg: "color_3",
      sidebarStyle: "full",
      sidebarPosition: "fixed",
      headerPosition: "fixed",
      containerLayout: "wide"
    },
    2: {
      typography: "cairo",
      version: "light",
      layout: "vertical",
      primary: "color_4",
      headerBg: "color_1",
      navheaderBg: "color_4",
      sidebarBg: "color_4",
      sidebarStyle: "compact",
      sidebarPosition: "fixed",
      headerPosition: "fixed",
      containerLayout: "wide"
    },
    3: {
      typography: "cairo",
      version: "light",
      layout: "vertical",
      primary: "color_7",
      headerBg: "color_1",
      navheaderBg: "color_7",
      sidebarBg: "color_7",
      sidebarStyle: "full",
      sidebarPosition: "fixed",
      headerPosition: "fixed",
      containerLayout: "wide"
    },
    4: {
      typography: "cairo",
      version: "dark",
      layout: "vertical",
      primary: "color_1",
      headerBg: "color_1",
      navheaderBg: "color_3",
      sidebarBg: "color_3",
      sidebarStyle: "full",
      sidebarPosition: "fixed",
      headerPosition: "fixed",
      containerLayout: "wide"
    },
    5: {
      typography: "cairo",
      version: "light",
      layout: "horizontal",
      primary: "color_5",
      headerBg: "color_1",
      navheaderBg: "color_1",
      sidebarBg: "color_5",
      sidebarStyle: "full",
      sidebarPosition: "fixed",
      headerPosition: "static",
      containerLayout: "wide"
    },
    6: {
      typography: "cairo",
      version: "light",
      layout: "vertical",
      primary: "color_10",
      headerBg: "color_1",
      navheaderBg: "color_1",
      sidebarBg: "color_10",
      sidebarStyle: "mini",
      sidebarPosition: "fixed",
      headerPosition: "fixed",
      containerLayout: "wide"
    },
    7: {
      typography: "cairo",
      version: "light",
      layout: "vertical",
      primary: "color_6",
      headerBg: "color_1",
      navheaderBg: "color_1",
      sidebarBg: "color_1",
      sidebarStyle: "compact",
      sidebarPosition: "fixed",
      headerPosition: "fixed",
      containerLayout: "wide"
    },
    8: {
      typography: "cairo",
      version: "light",
      layout: "vertical",
      primary: "color_15",
      headerBg: "color_1",
      navheaderBg: "color_15",
      sidebarBg: "color_15",
      sidebarStyle: "icon-hover",
      sidebarPosition: "fixed",
      headerPosition: "fixed",
      containerLayout: "wide"
    }
  };

  function setThemeInCookie(themeSettings) {
    jQuery.each(themeSettings, function (optionKey, optionValue) {
      setCookie(optionKey, optionValue);
    });
  }

  function syncSwitcherControls(settings) {
    if (!settings) return;
    $('#theme_version').val(settings.version || 'light');
    $('#theme_layout').val(settings.layout || 'vertical');
    $('#header_position').val(settings.headerPosition || 'fixed');
    $('#sidebar_style').val(settings.sidebarStyle || 'full');
    $('#sidebar_position').val(settings.sidebarPosition || 'fixed');
    $('#container_layout').val(settings.containerLayout || 'wide');
    $('#typography').val(settings.typography || 'cairo');

    if ($.fn.niceSelect) {
      $('.sidebar-right select.default-select').niceSelect('update');
    }

    if (settings.primary) {
      $('input[name="primary_bg"][value="' + settings.primary + '"]').prop('checked', true);
    }
    if (settings.navheaderBg) {
      $('input[name="navigation_header"][value="' + settings.navheaderBg + '"]').prop('checked', true);
    }
    if (settings.headerBg) {
      $('input[name="header_bg"][value="' + settings.headerBg + '"]').prop('checked', true);
    }
    if (settings.sidebarBg) {
      $('input[name="sidebar_bg"][value="' + settings.sidebarBg + '"]').prop('checked', true);
    }
  }

  function themeChange(themeIndex) {
    var themeSettings = $.extend({}, dezThemePresets[themeIndex] || dezThemePresets[0]);
    dezSettingsOptions = themeSettings;
    new dezSettings(themeSettings);
    if (themeSettings.headerBg) {
      $('body').attr('data-headerbg', themeSettings.headerBg);
    }
    setThemeInCookie(themeSettings);
    syncSwitcherControls(themeSettings);
  }

  function setThemeOptionOnPage() {
    if (getCookie('version') !== '') {
      jQuery.each(themeOptionArr, function (optionKey) {
        var optionData = getCookie(optionKey);
        themeOptionArr[optionKey] = (optionData !== '') ? optionData : (dezSettingsOptions[optionKey] || 'color_1');
      });
      dezSettingsOptions = $.extend({}, dezSettingsOptions, themeOptionArr);
      new dezSettings(dezSettingsOptions);
      if (dezSettingsOptions.headerBg) {
        $('body').attr('data-headerbg', dezSettingsOptions.headerBg);
      }
      syncSwitcherControls(dezSettingsOptions);
    } else {
      syncSwitcherControls(dezSettingsOptions);
    }
  }

  jQuery(document).on('click', '.dlab_theme_demo', function () {
    var demoTheme = jQuery(this).data('theme');
    themeChange(demoTheme);
    $('.dlab-demo-panel').removeClass('show');
  });

  jQuery(window).on('load', function () {
    if (theme !== undefined && dezThemePresets[theme]) {
      themeChange(theme);
    } else if (getCookie('version') === '') {
      themeChange(0);
    }
    setThemeOptionOnPage();
  });

})(jQuery);
