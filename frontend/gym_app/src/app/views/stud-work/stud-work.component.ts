import { Component } from '@angular/core';
import { ClasesService } from 'src/app/services/clases.service';
import { PlanificacionService } from 'src/app/services/planificacion.service';

@Component({
  selector: 'app-stud-work',
  templateUrl: './stud-work.component.html',
  styleUrls: ['./stud-work.component.css']
})
export class StudWorkComponent {

  // workoutItems = [
  //   {
  //     image: 'assets/clases/clase1.jpg',
  //     title: 'Clase 1',
  //     description: 'Fuerza',
  //     buttonText: 'Ver Clase'
  //   },
  //   {
  //     image: 'assets/clases/clase2.jpg',
  //     title: 'Clase 2',
  //     description: 'Fuerza',
  //     buttonText: 'Ver Clase'
  //   },
  //   {
  //     image: 'assets/clases/clase3.jpg',
  //     title: 'Clase 3',
  //     description: 'Fuerza',
  //     buttonText: 'Ver Clase'
  //   },
  // ];

  classItems: any[] = [];
  planItems: any[] = [];

  constructor(private clasesService: ClasesService, private planificacionService: PlanificacionService) {}

  ngOnInit(): void {
    const alumnoId = localStorage.getItem('id_alumno') ?? '';
    const alumnoIdNumber = parseInt(alumnoId, 10);

    this.planificacionService.getPlanificacionesPorAlumno(alumnoIdNumber).subscribe({
      next: (planificaciones) => {
        const uniqueClaseIds = [...new Set(planificaciones.map(item => item.id_clase))];
        for (const id of uniqueClaseIds) {
          this.getClaseName(id, planificaciones.filter(p => p.id_clase === id));
        }
      },
      error: (error) => {
        console.error('Error al obtener las planificaciones:', error);
      }
    });
  }

  getClaseName(id: number, planificaciones: any[]) {
    this.clasesService.getClassById(id).subscribe({
      next: (clase) => {
        console.log('clase:', clase);
        this.classItems.push({
          title: clase.tipo,
          planificaciones: planificaciones.map(p => ({
            title: `Planificación ${p.id_planificacion}`,
            description: `Objetivo: ${p.objetivo}, Nivel: ${p.nivel}, Horas Semanales: ${p.horas_semanales}`,
            buttonText: 'Ver Planificación',
            id_planificacion: p.id_planificacion
          }))
        });
      },
      error: (error) => {
        console.error('Error al obtener la clase:', error);
      }
    });
  }
}