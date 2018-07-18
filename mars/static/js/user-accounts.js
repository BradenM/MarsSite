var UserAccounts = (function () {

    // ====== UserAccounts Functions =======

    // Adjust Scrollable Div
    var adjustScroll = function () {
        var scrollDiv = $('section[data-scroll-adjust]');
        var tile = scrollDiv.find($('.is-child')).height();
        var tileNum = Math.ceil(scrollDiv.height() / tile)
        var tileAdjust = scrollDiv.height() - (tile * (tileNum - 4))
        scrollDiv.css('height', tileAdjust);
        scrollDiv.css('overflow-y', 'auto');
    }

    // Set Active Menu 
    var updateMenu = function () {
        var path = location.pathname
        var selectors = $('.menu li a')
        $.each(selectors, function () {
            if (path == $(this).attr('href')) {
                $(this).addClass('is-active');
                return false;
            }
        })
    }
    // ====== END UserAccounts Functions END =======

    // ====== Login & Security (Settings) ======
    var settingsPage = function () {
        // Init

        // Unlock Input
        $('a[data-unlock]').click(function (e) {
            unlockInput($(this));
        });

        // Allow Input Modify
        var unlockInput = function (trig) {
            var target_sel = trig.attr("data-unlock");
            var target_inp = $('#' + target_sel);
            // Allow Edit
            target_inp.removeAttr('readonly');
            // Change Trigger to 'save' and rebind
            trig.html('Save');
            // Unbind
            trig.off();
            // Bind to save
            trig.click(function (e) {
                saveInput(trig);
            })
        }

        // Save Input via Ajax
        var saveInput = function (trig) {
            var target_sel = trig.attr('data-unlock');
            var target_inp = $('#' + target_sel);
            // Get Form info
            var form = $('#' + target_inp.attr('form'))
            var form_data = form.find('input');
            var form_success = form.find('input[id=submit-id-submit]').attr('value');
            console.log(form_success)

            // Catch form post
            form.on('submit', function (e) {
                e.preventDefault();
                form_data.val(target_inp.val()); // Set new input to form val
                var ajax_data = form.serializeArray();
                // Append add action data for adding email
                ajax_data.push({
                    name: 'action_add',
                    value: ''
                })
                // Append CSRF token cookie
                ajax_data.push({
                    name: 'csrfmiddlewaretoken',
                    value: getCookie('csrftoken')
                })
                $.ajax({
                    url: form.attr('action'),
                    type: form.attr('method'),
                    data: ajax_data,
                    dataType: 'json',
                    success: function (data) {
                        target_inp.attr('readonly', '');
                        trig.html('Change');
                        // rebind
                        trig.off();
                        trig.click(function (e) {
                            unlockInput(trig);
                        })
                        n = infoNotify('Success!', form_success)
                        n.show();
                    },
                    error: function (data) {
                        console.log(data);
                        var json_fields = data.responseJSON.form.fields
                        //n = errorNotify(json_fields.email.errors);
                        var error_msg = []
                        $.each(json_fields, function (key, field) {
                            error_msg.push(field.errors);
                        })
                        n = errorNotify(error_msg);
                        n.show();
                    }
                })
            })

            // Submit
            form.submit();

        }

        // Change Password Ajax
        var loadChangePassword = function () {
            var change_passform = $('#auth_changepass');
            var loader = $('#pc_loader');
            var submit_button = $('#pcsubmit');
            change_passform.on('submit', function (e) {
                e.preventDefault();
                submit_button.addClass('is-hidden');
                loader.removeClass('is-hidden');
                $.ajax({
                    url: change_passform.attr('action'),
                    type: "POST",
                    dataType: 'json',
                    data: change_passform.serialize(),
                    success: function (data) {
                        location.reload();
                    },
                    error: function (data) {
                        console.log(data.responseJSON.form.fields);
                        // Short timeout to signify that request went through
                        setTimeout(function () {
                            $.each(data.responseJSON.form.fields, function (key, element) {
                                loader.addClass('is-hidden');
                                submit_button.removeClass('is-hidden');
                                var field = $('#pc_' + key + "_errors");
                                console.log(field);
                                field.html(element.errors);
                                console.log(element.errors);
                            });
                        }, 250)
                    }
                })
            })
        }
    }
    // ====== END Login & Security (Settings) END ======

    // ====== Payment Methods  ======
    var paymentsPage = function () {

        // Bind Card Expansion
        $('a.is-card-expand').click(function (e) {
            e.preventDefault();
            expandCard($(this))
        })

        // Bind Card Edit
        $('span[card-edit]').click(function (e) {
            e.preventDefault();
            editCard($(this)).hide();
        })

        // Card Expand
        var expandCard = function (trig) {
            var target = $('#' + trig.attr('data-expand'))
            target.slideToggle('fast');
            target.toggleClass('is-active');
            var icon = trig.find($('.icon'));
            icon.toggleClass('fa-rotate-180');
        }

        // Edit Card
        var editCard = function (trig) {
            // Vars
            var target = $('#' + trig.attr('card-edit'));
            var tar_form = target.find($('form'));
            // Get Inputs
            var inputs = target.find($('input'));
            // Get button siblings
            var siblingButtons = trig.parent().find($('span'));
            var cancel_edit = $(siblingButtons[1]);
            var cancel_default = cancel_edit.attr('onclick');

            // Toggle last button
            var displayLast = function (visibility, fade) {
                // Hide Last Button
                $(siblingButtons.last()).fadeTo(fade[0], fade[1], function () {
                    $(siblingButtons.last()).css('visibility', visibility);
                })
            }

            // Toggle form transition
            var transitionForm = function (status, input_display, input_type, fade) {
                // Change Edit button to 'save'
                trig.html(status[0]);
                cancel_edit.html(status[1])
                trig.toggleClass('is-primary');
                // Hide Infos
                $.each(inputs, function (i, el) {
                    var info = $(this).siblings('p');
                    info.fadeTo(fade[0], fade[1], function () {
                        info.css('display', input_display);
                        $(el).attr('type', input_type);
                    })
                })
            }

            var hide = function () {
                // Trans to Edit view
                displayLast('hidden', [200, 0]);
                transitionForm(['Save', 'Cancel'], 'none', 'text', [200, 0])
                // Rebind save to form submit
                trig.off();
                trig.click(function (e) {
                    e.preventDefault();
                    tar_form.submit();
                })
                // Bind target form to saveCard
                tar_form.on('submit', function (e) {
                    e.preventDefault();
                    saveCard(trig, tar_form);
                })
                // Bind cancel edit
                cancel_edit.attr('onclick', '');
                cancel_edit.on('click', function (e) {
                    e.preventDefault();
                    show();
                })
                // Load Cleave
                loadCleave().date();
            }

            var show = function () {
                // Trans to normal view
                displayLast('visible', [0, 200]);
                transitionForm(['Edit Card', 'Remove Card'], 'flex', 'hidden', [0, 200])
                // Unbind cancel edit
                cancel_edit.off();
                cancel_edit.attr('onclick', cancel_default);
                // Rebind edit card
                trig.off();
                trig.click(function (e) {
                    e.preventDefault();
                    hide();
                })
            }

            return {
                hide: hide
            }

        }

        // Save Card After Editing (w/ Ajax)
        var saveCard = function (source, targ) {
            source.addClass('is-loading');
            var name_error = $('#' + targ.attr('id') + '_name_error')
            var date_error = $('#' + targ.attr('id') + '_date_error')
            var ajax_data = handleAjax().prepareData(targ);
            var success = function (data) {
                source.removeClass('is-loading');
                location.reload();
            }
            var error = function (data) {
                source.removeClass('is-loading');
                var errors = data.responseJSON
                date_error.html(errors['date_errors']);
            }
            handleAjax().submitForm(targ, ajax_data, success, error)
        }

    }
    // ====== END Payment Methods END  ======

    // ====== Orders Page ======
    var ordersPage = function () {
        // Init
        var search_input = $('input[search-target]')
        var search = new SearchBar(search_input);
        search.bindEvents();
    }
    // ====== END Payment Methods END  ======

    // ====== Invoice Page ======
    var invoicePage = function () {
        // Order Scroll
        var orderScroll = function () {
            var scrollDivs = $(".is-scrollable")
            $.each(scrollDivs, function () {
                var orderTiles = $(this).find('.order-tile')
                var tileHeight = orderTiles.first().height();
                var adjust = (orderTiles.length - 4) * tileHeight;
                // Ignore anything that doesnt need to be resized
                if (adjust > 0) {
                    $(this).css('height', adjust)
                    $(this).css('overflow-y', 'auto')
                }
            })
        }
        orderScroll();
    }
    // ====== END Invoice Page ======


    updateMenu();
    adjustScroll();
    loadCleave().load();
    return {
        settingsPage: settingsPage,
        paymentsPage: paymentsPage,
        ordersPage: ordersPage,
        invoicePage: invoicePage
    }


})