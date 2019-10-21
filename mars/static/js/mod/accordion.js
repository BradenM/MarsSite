(function () {
    'use strict';
    const a = ['click', 'touchstart'];
    document.addEventListener('DOMContentLoaded', function () {
        var b = document.querySelectorAll('.accordions');
        [].forEach.call(b, function (b) {
            var c = b.querySelectorAll('.accordion');
            [].forEach.call(c, function (c) {
                a.forEach((a) => {
                    c.querySelector('.toggle, [data-action="toggle"]').addEventListener(a, (a) => {
                        if (a.preventDefault(), !c.classList.contains('is-active')) {
                            let a = b.querySelector('.accordion.is-active');
                            a && a.classList.remove('is-active'), c.classList.add('is-active')
                        } else c.classList.remove('is-active')
                    })
                })
            })
        })
    })
})();
//# sourceMappingURL=data:application/json;charset=utf8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInNyYy9leHRlbnNpb24uanMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6InlCQUFBLEtBQU0sQUFBWSxHQUFHLENBQUMsQUFBTyxRQUFFLEFBQVksQUFBQyxBQUFDLGNBRTdDLEFBQVEsU0FBQyxBQUFnQixpQkFBRSxBQUFrQixtQkFBRSxVQUFZLENBQ3pELEdBQUksQUFBVSxHQUFHLEFBQVEsU0FBQyxBQUFnQixpQkFBQyxBQUFhLEFBQUMsQUFBQyxlQUMxRCxBQUFFLEdBQUMsQUFBTyxRQUFDLEFBQUksQUFBQyxBQUFVLE9BQUUsQUFBUyxBQUFTLFdBQUUsQ0FDOUMsR0FBSSxBQUFLLEdBQUcsQUFBUyxFQUFDLEFBQWdCLGlCQUFDLEFBQVksQUFBQyxBQUFDLGNBQ3JELEFBQUUsR0FBQyxBQUFPLFFBQUMsQUFBSSxBQUFDLEFBQUssT0FBRSxBQUFTLEFBQUksV0FBRSxDQUNwQyxBQUFZLEVBQUMsQUFBTyxRQUFDLEFBQUMsQUFBSyxLQUFLLENBQzlCLEFBQUksRUFBQyxBQUFhLGNBQUMsQUFBaUMsQUFBQyxtQ0FBQyxBQUFnQixBQUFDLEFBQUssbUJBQUUsQUFBQyxLQUFJLENBRWpGLEdBREEsQUFBQyxFQUFDLEFBQWMsQUFBRSxBQUFDLGlCQUNmLENBQUMsQUFBSSxFQUFDLEFBQVMsVUFBQyxBQUFRLFNBQUMsQUFBVyxBQUFDLGFBQUUsQ0FDekMsR0FBSSxBQUFVLEdBQUcsQUFBUyxFQUFDLEFBQWEsY0FBQyxBQUFzQixBQUFDLEFBQUMsQUFDakUsQUFBSSxBQUFVLEFBQUUsMkJBQ2QsQUFBVSxFQUFDLEFBQVMsVUFBQyxBQUFNLE9BQUMsQUFBVyxBQUFDLEFBQUMsQUFDMUMsYUFDRCxBQUFJLEVBQUMsQUFBUyxVQUFDLEFBQUcsSUFBQyxBQUFXLEFBQUMsQUFBQyxZQUNqQyxBQUFNLEtBQ0wsQUFBSSxHQUFDLEFBQVMsVUFBQyxBQUFNLE9BQUMsQUFBVyxBQUFDLEFBQUMsQUFDcEMsWUFDRixBQUFDLEFBQUMsRUFDSixBQUFDLEFBQUMsRUFDSixBQUFDLEFBQUMsRUFDSixBQUFDLEFBQUMsRUFDSixBQUFDLEFBQUMiLCJmaWxlIjoiYnVsbWEtYWNjb3JkaW9uLm1pbi5qcyIsInNvdXJjZXNDb250ZW50IjpbImNvbnN0IE1PVVNFX0VWRU5UUyA9IFsnY2xpY2snLCAndG91Y2hzdGFydCddO1xuXG5kb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKCAnRE9NQ29udGVudExvYWRlZCcsIGZ1bmN0aW9uICgpIHtcbiAgdmFyIGFjY29yZGlvbnMgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yQWxsKCcuYWNjb3JkaW9ucycpO1xuICBbXS5mb3JFYWNoLmNhbGwoYWNjb3JkaW9ucywgZnVuY3Rpb24oYWNjb3JkaW9uKSB7XG4gICAgdmFyIGl0ZW1zID0gYWNjb3JkaW9uLnF1ZXJ5U2VsZWN0b3JBbGwoJy5hY2NvcmRpb24nKTtcbiAgICBbXS5mb3JFYWNoLmNhbGwoaXRlbXMsIGZ1bmN0aW9uKGl0ZW0pIHtcbiAgICAgIE1PVVNFX0VWRU5UUy5mb3JFYWNoKChldmVudCkgPT4ge1xuICAgICAgICBpdGVtLnF1ZXJ5U2VsZWN0b3IoJy50b2dnbGUsIFtkYXRhLWFjdGlvbj1cInRvZ2dsZVwiXScpLmFkZEV2ZW50TGlzdGVuZXIoZXZlbnQsIGUgPT4ge1xuICAgICAgICAgIGUucHJldmVudERlZmF1bHQoKTtcbiAgICAgICAgICBpZiAoIWl0ZW0uY2xhc3NMaXN0LmNvbnRhaW5zKCdpcy1hY3RpdmUnKSkge1xuICAgICAgICAgICAgbGV0IGFjdGl2ZUl0ZW0gPSBhY2NvcmRpb24ucXVlcnlTZWxlY3RvcignLmFjY29yZGlvbi5pcy1hY3RpdmUnKTtcbiAgICAgICAgICAgIGlmIChhY3RpdmVJdGVtKSB7XG4gICAgICAgICAgICAgIGFjdGl2ZUl0ZW0uY2xhc3NMaXN0LnJlbW92ZSgnaXMtYWN0aXZlJyk7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBpdGVtLmNsYXNzTGlzdC5hZGQoJ2lzLWFjdGl2ZScpO1xuICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICBpdGVtLmNsYXNzTGlzdC5yZW1vdmUoJ2lzLWFjdGl2ZScpO1xuICAgICAgICAgIH1cbiAgICAgICAgfSk7XG4gICAgICB9KTtcbiAgICB9KTtcbiAgfSk7XG59KTtcbiJdfQ==