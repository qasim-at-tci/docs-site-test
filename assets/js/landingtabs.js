// NK - Tabs implementation taken from https://github.com/fluxcd/website 
// Copyright 2021 fluxcd.io
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// http://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

var $ = window.$;

$('.tab-content').find('.tab-pane').each(function (idx, item) {
  var navTabs = $(this).closest('.code-tabs').find('.nav-tabs');
  var title = $(this).attr('title');
  navTabs.append('<li class="nav-tab tabby"><a href="#" class="nav-tab">' + title + '</a></li>');
});

$('.code-tabs ul.nav-tabs').each(function () {
  $(this).find('li:first').addClass('active');
});

$('.code-tabs .tab-content').each(function () {
  $(this).find('div:first').addClass('active');
});

$('.nav-tabs a').click(function (e) {
  e.preventDefault();
  var tab = $(this).parent();
  var tabIndex = tab.index();
  var tabPanel = $(this).closest('.code-tabs');
  var tabPane = tabPanel.find('.tab-pane').eq(tabIndex);
  tabPanel.find('.active').removeClass('active');
  tab.addClass('active');
  tabPane.addClass('active');
});
