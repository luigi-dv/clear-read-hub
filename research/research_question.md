# Research question and hypotheses (draft 1)

Status: draft for the author to edit. Nothing here is final until the evidence matrix
is complete and the hypotheses are preregistered.

## Working title

Attention re-engagement in document reading: do presentation-level cues improve
comprehension for adults with ADHD?

## Problem

Adults with ADHD decode words normally but build a weaker model of a document: they
re-read more, mind-wander more, and lose central ideas rather than details
(evidence matrix M1 to M6). Reading tools marketed to ADHD users (chunking, fonts,
Bionic Reading, reader modes) rest on dyslexia or general-reader evidence, or on
null results (I6, H4, N1). Only text-to-speech and metacognitive scaffolding have
ADHD-specific comprehension evidence (I3, I5), and no readability corpus carries
judgements from ADHD readers.

## Research question

For adults with ADHD reading long expository documents on screen, which
presentation-level cues reduce attentional lapses and improve comprehension of
central ideas, compared with an unmodified document?

## Candidate interventions (pick three or four after the matrix is complete)

| Code | Intervention | Mechanism it targets | Prior evidence |
| --- | --- | --- | --- |
| C0 | Unmodified document (control) | none | baseline |
| C1 | Keyword / central-idea highlighting | working-memory load, gist retrieval | I1 (3 ADHD children), I2 (dyslexia) |
| C2 | Chunking into short sections with headings | sustained attention, unfinished reading | general-reader and dyslexia evidence only |
| C3 | Re-engagement prompts (brief self-monitoring questions between sections) | mind-wandering, meta-awareness | I5 (210 adults, gap eliminated), I4 |
| C4 | Text-to-speech with synchronised highlighting | sustained attention, modality | I3 |
| C5 | Reader-adjustable presentation (participant chooses parameters) | personal fit | I6, H1 |

C3 is the strongest candidate on evidence. C1 is the most under-tested and the one
the project can implement as a model. C5 is a different study design (personalisation)
and should probably be a second study.

## Hypotheses (to be preregistered)

- H1. Comprehension of central ideas is higher under each cue condition than under C0
  for participants with ADHD.
- H2. The benefit of the cues is larger for participants with ADHD than for
  participants without ADHD (group by condition interaction).
- H3. Probe-caught mind-wandering is lower under the cue conditions than under C0.
- H4. Re-reading, measured as sections revisited, is lower under the cue conditions.
- H5 (exploratory). Reading speed does not predict comprehension in the ADHD group
  (H1 in the matrix found ADHD readers faster with worse comprehension).

## Primary and secondary outcomes

- Primary: comprehension of central ideas, scored from short-answer recall of
  main points, with a separate score for peripheral details.
- Primary: mind-wandering frequency from thought probes inserted at fixed points.
- Secondary: time on task, sections revisited (re-reading), NASA-TLX workload,
  condition preference, confidence versus actual score (self-monitoring).
- Not an outcome: words per minute as a measure of success.

## Population and screening

- Adults 18 to 50. ADHD group: self-reported diagnosis plus ASRS v1.1 screener at or
  above threshold. Control group: ASRS below threshold, no diagnosis.
- Report diagnosis source, medication status on the day, and a short decoding check
  to screen out undiagnosed dyslexia (25 to 40 percent comorbidity).
- Target: 24 to 36 ADHD participants and a matched control group. The accessibility
  field median is 13, so this exceeds the norm. Confirm with a paired-design power
  calculation once the pilot gives an effect-size estimate.

## Design

- Within-subject, each participant reads one matched long expository passage per
  condition, condition order and passage assignment counterbalanced with a Latin
  square. Passages matched on length, Flesch-Kincaid grade and topic familiarity.
- Online delivery through Clear Read Hub so the interface conditions are the ones
  the product will ship. Pilot with five non-ADHD readers first to remove bugs.

## What the model would learn, once data exists

- Option A: predict, per sentence, whether it is a central idea, trained on the
  passages and the recall data, to drive C1 automatically.
- Option B: predict, per document position, where re-reading and probe-caught lapses
  cluster, to drive where C3 prompts are inserted.
- Option C: predict per-reader presentation parameters from a short calibration
  reading (the C5 study).

## Open decisions for the author

1. Ethics route: partner university or commercial review board.
2. Recruitment: Prolific with ADHD prescreen, ADHD communities, or clinic referral.
3. Language of the passages: English (most instruments) or Spanish (local recruitment).
4. Which three or four conditions to run first.
