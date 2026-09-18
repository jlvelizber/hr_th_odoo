# Facturacion electronica SRI — Fase 3

Modulo: `l10n_ec_th_edi`

## Implementado

- Trazabilidad `sri.ec.document` ligada a `account.move`
- Estados: borrador → XML → firmado → recepcion/autorizacion (simulacion)
- Configuracion compania: ambiente, nota certificado
- Menu Contabilidad → SRI Ecuador

## Pendiente (integracion completa)

Seguir skill SRI Ecuador offline: XML 1.1.0, clave 49 digitos, XAdES-BES, SOAP celcer/cel, RIDE PDF.

No hardcodear certificados en el repositorio.
