{{/*
Expand the name of the chart.
*/}}
{{- define "je-deel-test.fullname" -}}
{{- .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end -}}
