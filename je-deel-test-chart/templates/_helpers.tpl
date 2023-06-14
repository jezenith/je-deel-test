{{/*
Common labels
*/}}
{{- define "je-deel-test.labels" -}}
helm.sh/chart: {{ include "je-deel-test.chart" . }}
{{ include "je-deel-test.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{/*
Selector labels
*/}}
{{- define "je-deel-test.selectorLabels" -}}
app.kubernetes.io/name: {{ include "je-deel-test.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{/*
Chart label
*/}}
{{- define "je-deel-test.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end -}}
