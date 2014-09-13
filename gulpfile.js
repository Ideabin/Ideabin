// Gulp plugins
var gulp = require('gulp'),
    watch = require('gulp-watch'),
    minifycss = require('gulp-minify-css'),
    less = require('gulp-less');

// Compile less files to css
gulp.task('less', function() {
    return gulp.src('frontend/static/less/styles.less')
        .pipe(less())
        .pipe(gulp.dest('frontend/static/css'))
});

// Run tasks when files in 'static' directory change
gulp.task('watch', function() {
    gulp.watch('static/less/**', ['less']);
});

gulp.task('default', ['less', 'watch']);
