import { computed } from 'vue';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { RadarChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  RadarComponent
} from 'echarts/components';

use([
  CanvasRenderer,
  RadarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  RadarComponent
]);

const labels = [
  'Salud',
  'Personalidad',
  'Intelecto',
  'Carrera',
  'Finanzas',
  'Calidad de Vida',
  'Emocionalidad',
  'Relaciones'
];

export function useChartOptions(props: { values?: number[] }) {
  const chartValues = computed(() => props.values && props.values.length === 8 ? props.values : [80, 60, 70, 30, 40, 50, 20, 60]);

  const chartOption = computed(() => ({
    backgroundColor: '#090f20', // Establece el color de fondo del gráfico
    tooltip: {},
    radar: {
      indicator: labels.map(label => ({ name: label, max: 100 })),
      radius: '70%', // Ajusta el tamaño del radar
      center: ['50%', '50%'], // Centra el radar
      axisName: {
        color: '#fff', // Color blanco para los labels de los ejes
        fontSize: 12,
        fontFamily: 'Orbitron, sans-serif',
        formatter: function (value: string) {
          // Ajuste manual para "Emocionalidad" si es necesario, o para todos los labels
          if (value === 'Emocionalidad') {
            return '{a|' + value + '}';
          }
          return value;
        },
        rich: {
          a: {
            // Estilos específicos para "Emocionalidad" si se necesita un ajuste fino
            // Por ejemplo, para moverlo un poco más
            // padding: [0, 0, 0, 10]
          }
        }
      },
      axisLine: {
        lineStyle: {
          color: '#1e293b' // gray-800
        }
      },
      splitLine: {
        lineStyle: {
          color: '#1e293b' // gray-800
        }
      },
      splitArea: {
        areaStyle: {
          color: ['rgba(255, 255, 255, 0.05)', 'rgba(255, 255, 255, 0.02)'] // Colores de las áreas concéntricas, más sutiles
        }
      }
    },
    series: [
      {
        name: 'Progreso Vital',
        type: 'radar',
        data: [
          {
            value: chartValues.value,
            name: 'Progreso',
            areaStyle: {
              opacity: 0.5,
              color: '#38bdf8' // sky-400
            },
            lineStyle: {
              color: '#38bdf8' // sky-400
            }
          }
        ]
      }
    ]
  }));

  return { chartOption };
}
