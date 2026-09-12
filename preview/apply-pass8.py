#!/usr/bin/env python3
"""Pass 8: estimate page mobile split (verbatim sentences)."""
import sys
from pathlib import Path

est_path = Path('/home/mrh/real-estate-consulting/site/preview/estimate-preview.html')
est = est_path.read_text()

old = ('<p>Projected appointments come from your audit: your workable lead count against published '
       'reactivation benchmarks, as a band, not a promise. Cost is that band at the per-appointment '
       'rate of $60. Real results can land anywhere in the band or outside it, which is why nothing '
       'is charged unless appointments actually book.</p>')
new = ('<p>Projected appointments come from your audit: your workable lead count against published '
       'reactivation benchmarks, as a band, not a promise. Cost is that band at the per-appointment '
       'rate of $60.</p><p>Real results can land anywhere in the band or outside it, which is why '
       'nothing is charged unless appointments actually book.</p>')
assert est.count(old) == 1, 'anchor not unique'
est_path.write_text(est.replace(old, new))
print('PASS-8 DONE')
