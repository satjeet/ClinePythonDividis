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

import iconMapJsonRaw from '@/assets/icons/icon-map.json';
const iconMapJson = iconMapJsonRaw as Record<string, string>;

const labels = [
  'Salud',           // 12:00
  'Relaciones',      // 1:30
  'Emocionalidad',   // 3:00
  'Calidad de Vida', // 4:30
  'Finanzas',        // 6:00
  'Carrera',         // 7:30
  'Intelecto',       // 9:00
  'Personalidad'     // 10:30
];

// Mapeo de label a ruta SVG
const labelSvgMap: Record<string, string> = {};
for (const label of labels) {
  labelSvgMap[label] = new URL(`../../assets/icons/${iconMapJson[label]}`, import.meta.url).href;
}

// Mapeo de label a icono FontAwesome
const labelIconMap: Record<string, string> = {
  'Salud': 'fas fa-heartbeat',
  'Personalidad': 'fas fa-user-astronaut',
  'Intelecto': 'fas fa-brain',
  'Carrera': 'fas fa-rocket',
  'Finanzas': 'fas fa-coins',
  'Calidad de Vida': 'fas fa-star',
  'Emocionalidad': 'fas fa-spa',
  'Relaciones': 'fas fa-users'
};

export function useChartOptions(props: { values?: number[] }) {
  const chartValues = computed(() => props.values && props.values.length === 8 ? props.values : [80, 60, 70, 30, 40, 50, 20, 60]);

  const chartOption = computed(() => {
    // Responsive: reducir el radius en mobile
    const isMobile = typeof window !== 'undefined' && window.innerWidth < 640;
    const radarRadius = isMobile ? '45%' : '50%';
    const radarCenter = ['50%', '50%'];

    // Leer colores del theme activo
    let themeBg = '';
    let themeAccent = '';
    let themeBorder = '';
    let themeFont = '';
    let themeAccentContrast = '';
    if (typeof window !== 'undefined') {
      const style = getComputedStyle(document.body);
      themeBg = style.getPropertyValue('--theme-bg')?.trim();
      themeAccent = style.getPropertyValue('--theme-accent')?.trim();
      themeBorder = style.getPropertyValue('--theme-border')?.trim();
      themeFont = style.getPropertyValue('--theme-font')?.trim();
      themeAccentContrast = style.getPropertyValue('--theme-accent-contrast')?.trim();
    }
    // Si el fondo es vacío o gradiente, usar transparente
    if (!themeBg || themeBg.startsWith('linear-gradient')) {
      themeBg = 'transparent';
    }

    return {
      backgroundColor: themeBg,
      tooltip: {},
      radar: {
        indicator: labels.map(label => ({
          name: label,
          max: 100,
          icon: labelIconMap[label] || 'fas fa-star'
        })),
        radius: radarRadius, // Responsive
        center: radarCenter, // Responsive
        axisName: {
          color: themeAccentContrast,
          fontSize: isMobile ? 6 : 14,
          fontFamily: themeFont,
          formatter: function (value: string) {
            if (isMobile) {
              // Usar abreviatura de 2 letras para mobile
              return value.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();
            }
            return value;
          },
          rich: {
            icon: {
              height: 18,
              width: 18,
              backgroundColor: {
                image: (function () {
                  if (typeof window !== 'undefined' && window.innerWidth < 640) {
                    // Workaround: usar el primer icono (todos los labels mostrarán el mismo)
                    return labelSvgMap[labels[0]];
                  }
                  return '';
                })()
              }
            }
          }
        },
        axisLine: {
          lineStyle: {
            color: themeBorder
          }
        },
        splitLine: {
          lineStyle: {
            color: themeBorder
          }
        },
        splitArea: {
          areaStyle: {
            color: [
              themeAccent + '10', // 10% opacity
              themeAccent + '05'  // 5% opacity
            ]
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
                color: themeAccent
              },
              lineStyle: {
                color: themeAccent
              }
            }
          ]
        }
      ]
    };
  });

  return { chartOption };
}
