import { Component, OnInit } from '@angular/core';
import { CourseService, Course } from '../course.service';

@Component({
  selector: 'app-course-list',
  templateUrl: './course-list.component.html',
  styleUrls: ['./course-list.component.css']
})
export class CourseListComponent implements OnInit {
  courses: Course[] = [];
  searchTerm = '';
  loading = false;

  // Task 2, step 98: CourseService injected via the constructor.
  constructor(private courseService: CourseService) {}

  ngOnInit(): void {
    // Task 2, step 99-100: subscribe to the service Observable, toggle
    // the loading flag before/after the call resolves.
    this.loading = true;
    this.courseService.getCourses().subscribe({
      next: (data) => {
        this.courses = data;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      },
    });
  }

  get filteredCourses(): Course[] {
    // Task 1, step 94: filters the list as searchTerm (bound via ngModel) changes.
    return this.courses.filter((course) =>
      course.name.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }
}
