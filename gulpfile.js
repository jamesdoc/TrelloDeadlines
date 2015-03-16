var gulp = require('gulp'),
    compass = require('gulp-compass'),
    path = require('path');

gulp.task('compass', function() {
    gulp.src('assets/sass/*.scss')
    .pipe(compass({
        config_file: 'config.rb',
        css: 'www/build/css',
        sass: 'assets/sass'
    }))
    .pipe(gulp.dest('temp'));
});

gulp.task('default', ['compass']);