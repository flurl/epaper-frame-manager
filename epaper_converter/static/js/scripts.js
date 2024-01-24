/******************
 * jQuery replacement
 *******************/
if (typeof $ == "undefined") {
    !function (b, c, d, e, f) {
        f = b['add' + e]
        function i(a, d, i) {
            for (d = (a && a.nodeType ? [a] : '' + a === a ? b.querySelectorAll(a) : c), i = d.length; i--; c.unshift.call(this, d[i]));
        }
        $ = function (a) {
            return /^f/.test(typeof a) ? /in/.test(b.readyState) ? setTimeout(function () {
                $(a);
            }, 9) : a() : new i(a);
        };
        $[d] = i[d] = {
            on: function (a, b) {
                return this.each(function (c) {
                    f ? c['add' + e](a, b, false) : c.attachEvent('on' + a, b)
                })
            },
            off: function (a, b) {
                return this.each(function (c) {
                    f ? c['remove' + e](a, b) : c.detachEvent('on' + a, b)
                })
            },
            each: function (a, b) {
                for (var c = this, d = 0, e = c.length; d < e; ++d) {
                    a.call(b || c[d], c[d], d, c)
                }
                return c
            },
            splice: c.splice
        }
    }(document, [], 'prototype', 'EventListener');
    var props = ['add', 'remove', 'toggle', 'has'],
        maps = ['add', 'remove', 'toggle', 'contains'];
    props.forEach(function (prop, index) {
        $.prototype[prop + 'Class'] = function (a) {
            return this.each(function (b) {
                if (a) {
                    b.classList[maps[index]](a);
                }
            });
        };
    });
}


$.prototype.find = function (selector) {
    return $(selector, this);
};
$.prototype.parent = function () {
    return (this.length == 1) ? $(this[0].parentNode) : [];
};
$.prototype.first = function () {
    return $(this[0]);
};
$.prototype.focus = function () {
    return this[0].focus();
};
$.prototype.css = function (a, b) {
    if (typeof (a) === 'object') {
        for (var prop in a) {
            this.each(function (c) {
                c.style[prop] = a[prop];
            });
        }
        return this;
    } else {
        return b === []._ ? this[0].style[a] : this.each(function (c) {
            c.style[a] = b;
        });
    }
};
$.prototype.text = function (a) {
    return a === []._ ? this[0].textContent : this.each(function (b) {
        b.textContent = a;
    });
};

$.prototype.attr = function (a, b) {
    return b === []._ ? this[0].getAttribute(a) : this.each(function (c) {
        c.setAttribute(a, b);
    });
};
$.param = function (obj, prefix) {
    var str = [];
    for (var p in obj) {
        var k = prefix ? prefix + "[" + p + "]" : p, v = obj[p];
        str.push(typeof v == "object" ? $.param(v, k) : encodeURIComponent(k) + "=" + encodeURIComponent(v));
    }
    return str.join("&");
};
$.prototype.append = function (a) {
    return this.each(function (b) {
        b.appendChild(a[0]);
    });
};
$.ajax = function (a, b, c, d) {
    var xhr = new XMLHttpRequest();
    var type = (typeof (b) === 'object') ? 1 : 0;
    var gp = ['GET', 'POST'];
    xhr.open(gp[type], a, true);
    if (type == 1) {
        xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    }
    xhr.responseType = (typeof (c) === 'string') ? c : '';
    var cb = (!type) ? b : c;
    xhr.onerror = function () {
        cb(this, true);
    };
    xhr.onreadystatechange = function () {
        if (this.readyState === 4) {
            if (this.status >= 200 && this.status < 400) {
                cb(this, false);
            } else {
                cb(this, true);
            }
        }
    };
    if (d) {
        for (const header in d) {
            xhr.setRequestHeader(header, d[header]);
        }
    }
    if (type) {
        xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        xhr.send($.param(b));
    } else {
        xhr.send();
    }
    xhr = null;
};
/*****************
* end jQuery replacement
*******************/

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


const IMG_WIDTH = 448;
const IMG_HEIGHT = 600;

class Editor {
    #cropper = null;
    #imageSrc = null;
    #imageId = null;

    constructor () {
        $('.overlay-close').on('click', this.closeOverlay.bind(this));
        $('.overlay-controls .edit-button').on('click', this.#editImage.bind(this));
        $('.overlay-controls .delete-button').on('click', this.#deleteImage.bind(this));
    }
    
    #convertImagePath(path) {
        var directories = path.split('/');
        var filename = directories.pop();
        var filenameParts = filename.split('.');
        filenameParts[filenameParts.length - 1] = 'bmp';
        var newFilename = filenameParts.join('.');
        directories.push('converted');
        directories.push(newFilename);
        var newPath = directories.join('/');
        return newPath;
    }    
    
    #editImage() {
        let src = this.#imageSrc;
        $("#overlay-image").attr("src", src);
        const image = document.getElementById('overlay-image');
        this.#cropper = new Cropper(image, {
            aspectRatio: IMG_WIDTH / IMG_HEIGHT,
            viewMode: 1,
            crop(event) {
                console.log('x: ' + event.detail.x);
                console.log('y: ' + event.detail.y);
                console.log('w: ' + event.detail.width);
                console.log('h: ' + event.detail.height);
                console.log(event.detail.rotate);
                console.log(event.detail.scaleX);
                console.log(event.detail.scaleY);
            },
        });
        $('.overlay .rotate-left-button').on('click', () => this.#cropper.rotate(-90));
        $('.overlay .rotate-right-button').on('click', () => this.#cropper.rotate(90));
        $('.overlay .cancel-button').on('click', () => this.cancelEdit());
        $('.overlay .save-button').on('click', () => this.saveImage());
        this.#toggleControls();
    }


    #deleteImage() {
        if (confirm('Are you sure that you want to delete this image?')) {
            fetch(`/images/delete/${this.#imageId}`)
            .then(response => {
                alert('Image deleted.');
                document.location.reload();
            }).catch(reason => {
                alert('Failed to delete the image!');
            });
        }
    }


    #toggleControls() {
        $('.overlay .overlay-controls').toggleClass('hidden');
        $('.overlay .overlay-editor-controls').toggleClass('hidden');
    }


    cancelEdit() {
        try {
            this.#cropper.destroy();
        } catch {}
        $("#overlay-image").attr("src", this.#convertImagePath(this.#imageSrc));
        this.#toggleControls();
    }

    saveImage() {
        const csrftoken = getCookie('csrftoken');
        // const url = new URL(this.#imageSrc);
        // const src = url.pathname;
        const src = this.#imageSrc;
        const cropData = this.#cropper.getData();
        $.ajax('/images/convert',
            {
                'image': src,
                'offsetX': cropData.x,
                'offsetY': cropData.y,
                'width': cropData.width,
                'height': cropData.height,
                'rotate': cropData.rotate,
                'csrftoken': csrftoken
            },
            (xhr, error) => {
                if (error) {
                    alert('An error occured while saving the image.')
                }
                this.cancelEdit()
            },
            {
                'X-CSRFToken': csrftoken
            }
        );
    }
    
    
    openImageInOverlay(src, id) {
        this.#imageSrc = src;
        this.#imageId = id;
        $('.overlay .overlay-controls').removeClass('hidden');
        $('.overlay .overlay-editor-controls').addClass('hidden');
        $("#overlay-image").attr("src", this.#convertImagePath(src));
        $('.overlay').removeClass('hidden');
    }

    closeOverlay() {
        this.cancelEdit();
        $('.overlay').addClass('hidden');
    }

};

 const editor = new Editor();


$(() => {
    // $('.overlay').addClass('hidden');
    $('#images-list .images-list-image-container').on('click', (e) => {
        let src = e.target.style.backgroundImage.split('"')[1];
        let id = e.target.dataset.imageId;
        editor.openImageInOverlay(src, id);
    });
});