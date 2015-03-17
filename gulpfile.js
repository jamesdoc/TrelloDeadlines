var gulp = require('gulp'),
    compass = require('gulp-compass'),
    path = require('path'),
    watch = require('gulp-livereload');

gulp.task('compass', function() {
    gulp.src('assets/sass/*.scss')
    .pipe(compass({
        config_file: 'config.rb',
        css: 'www/build/css',
        sass: 'assets/sass'
    }))
    .pipe(gulp.dest('temp'));
});

gulp.task('test', function () {
   console.log('test test test');
});

gulp.task('watch', function() {
    gulp.watch('assets/sass/*.scss', ['compass']);
});

gulp.task('default', ['compass']);