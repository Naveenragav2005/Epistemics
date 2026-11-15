# Answer-key flags

54 of 994 items: every model that screened them (deepseek-v4-flash, gemma-4-31b-it, qwen3.5-397b; at least 2 per item) agrees on a non-key answer.

Set each verdict in `data/key_audit.jsonl`. Excluded verdicts: ambiguous, key_wrong.

## mmlupro-10421 (computer science): **ambiguous**

Suppose your model is overfitting. Which of the following is NOT a valid way to try and reduce the overfitting?

- Key (C): Improve the optimisation algorithm being used for error minimisation.
- Models (E): Increase the model complexity.
- Note: Both 'improve the optimiser' (key) and 'increase model complexity' (consensus) fail to reduce overfitting. Reviewer: Claude, needs human confirmation.

## mmlupro-10633 (computer science): **ambiguous**

When doing least-squares regression with regularisation (assuming that the optimisation can be done exactly), increasing the value of the regularisation parameter λ the testing error.

- Key (I): will never decrease the training error.
- Models (C): may decrease or increase the testing error.
- Note: Stem asks about testing error but the key speaks of training error; key and consensus are both true statements. Reviewer: Claude, needs human confirmation.

## mmlupro-11082 (philosophy): **ambiguous**

What is the "intergenerational storm" of climate change?

- Key (J): the problem that countries are possibly biased toward the interests of the current generation, which largely benefits from carbon dioxide emissions.
- Models (I): the problem that the bad effects of current carbon dioxide emissions will fall largely on future generations.
- Note: Gardiner's 'intergenerational storm' covers both current-generation bias and costs falling on future generations; key and consensus each capture part. Reviewer: Claude, needs human confirmation.

## mmlupro-1721 (law): **ambiguous**

A state legislature passed a law requiring state universities to have male and female students live in separate dormitory facilities. The law was passed in order to curtail the increasing number of co-ed pregnancies on college campuses. Two students at a state university are engaged to be married and wish to share a dormitory room together. Citing the law, university housing officials refuse to allow them to live together in a campus dormitory facility. The students bring an appropriate action to challenge the constitutionality of the law. Which of the following correctly states the applicable burden of persuasion?

- Key (A): Since the law does not affect a fundamental right or involve gender discrimination, the burden is on the plaintiffs to show that it is not rationally related to a legitimate governmental interest.
- Models (E): Since the law involves gender discrimination, the state must prove that the law is substantially related to an important state interest.
- Note: A sex-segregated dorm rule is arguably a gender classification (intermediate scrutiny, consensus E); key A treats it as rational basis. Contestable. Reviewer: Claude, needs human confirmation.

## mmlupro-242 (business): **ambiguous**

On January 1, 1964, Stead and Company purchased a delivery truck for $4,000. It is estimated that the truck will have a useful life of four years, and that at the end of that time it will have a salvage value (resale value) of $400. It is expected that the truck will be used for 72,000 miles. Find the depreciation per year, if the truck was used for 20,000 miles during the first year, 25,000 miles during the second year, 18,000 miles during the third year and 9,000 miles during the fourth year. Use the units of production method for determining depreciation.

- Key (H): $3,600.00
- Models (B): $1,000.00
- Note: Stem asks for 'depreciation per year' but the per-year units-of-production figures differ (1000/1250/900/450); key is the total depreciable base. Reviewer: Claude, needs human confirmation.

## mmlupro-6415 (health): **ambiguous**

Which of the following karyotypes is diagnostic of Down syndrome

- Key (E): 46,XX,der(14;21)(q10;q10)pat+21
- Models (H): 47,XX,+21
- Note: Both trisomy 21 (47,XX,+21) and a Robertsonian translocation karyotype are diagnostic of Down syndrome. Reviewer: Claude, needs human confirmation.

## mmlupro-7365 (economics): **ambiguous**

Which of the following examples would result in consumers paying for the largest burden of an excise tax placed on a producer?

- Key (F): If the demand curve is perfectly inelastic and the supply curve is price elastic
- Models (G): If the demand curve is perfectly inelastic and the supply curve is perfectly elastic
- Note: With perfectly inelastic demand, consumers bear 100% of the tax whatever the supply elasticity, so F and G are both fully correct. G is the more standard textbook answer. Reviewer: Claude.

## mmlupro-7443 (economics): **ambiguous**

Which characteristic is likely a part of a monopoly market but not of monopolistic competition?

- Key (F): Patents and copyrights
- Models (E): High barriers to entry
- Note: High barriers to entry and patents/copyrights both distinguish monopoly from monopolistic competition. Reviewer: Claude, needs human confirmation.

## mmlupro-7511 (economics): **ambiguous**

Consider the following AR(2) process:

yt = 1.5 yt-1 - 0.5 yt-2 + ut

This is a

- Key (B): Unit root process
- Models (A): Non-stationary and unit root process
- Note: Roots 1 and 2: the process is both a unit root process and non-stationary, so both options hold. Reviewer: Claude, needs human confirmation.

## mmlupro-8028 (math): **ambiguous**

The first number in a number pattern is 28. The pattern rule is to add 14 to get the next number in the pattern. If the pattern continues, which statement is true?

- Key (I): All the numbers in the pattern can be divided equally by 7.
- Models (D): All the numbers in the pattern can be divided equally by 14.
- Note: 28, 42, 56... are divisible by both 14 and 7. Reviewer: Claude, needs human confirmation.

## mmlupro-9517 (physics): **ambiguous**

For a uniform sphere with moments of inertia I_1 = I_2 = I_3, use the Euler equations to find the equation of motion of the sphere.

- Key (A): \omega = const
- Models (I): \dot{\omega} = 0
- Note: omega = const and d(omega)/dt = 0 are equivalent. Reviewer: Claude, needs human confirmation.

## mmlupro-9578 (physics): **ambiguous**

Six simple harmonic motions, each of the same amplitude and period, acting along the same straight line, are superimposed. If the phase difference between each successive pair is the same, find one value of this phase difference for which the resultant amplitude is zero.

- Key (A): 120 degrees
- Models (F): 60 degrees
- Note: Both 60 and 120 degrees give zero resultant amplitude for six equal phasors. Reviewer: Claude, needs human confirmation.

## mmlupro-10599 (computer science): **key_ok**

The disadvantage of Grid search is

- Key (F): It runs reasonably slow for multiple linear regression.
- Models (C): It is not suitable for datasets with a large number of features.
- Note: Key is the original MMLU answer. Oddly worded, but it is the intended one; C is not a standard disadvantage of grid search. Reviewer: Claude, needs human confirmation.

## mmlupro-5045 (history): **key_ok**

This question refers to the following information.
"If any person or persons shall, from and after the passing of this act, by force and violence, take and carry away, or cause to be taken or carried away, and shall, by fraud or false pretense, seduce, or cause to be seduced, or shall attempt so to take, carry away or seduce, any negro or mulatto, from any part or parts of this commonwealth, to any other place or places whatsoever, out of this commonwealth, with a design and intention of selling and disposing of, or of causing to be sold, or of keeping and detaining, or of causing to be kept and detained, such negro or mulatto, as a slave or servant for life, or for any term whatsoever, every such person or persons, his or their aiders or abettors, shall on conviction thereof, in any court of this commonwealth having competent jurisdiction, be deemed guilty of a felony."
—Excerpt from Pennsylvania law, 1826
The passage and implementation of this Pennsylvania law reflected an ongoing conflict between

- Key (E): federal law and state law.
- Models (G): Northern and Southern states over the issue of slavery.
- Note: 1826 Pennsylvania anti-kidnapping law reflects the federal vs state conflict (Prigg v. Pennsylvania). Reviewer: Claude, needs human confirmation.

## mmlupro-7653 (economics): **key_ok**

Which of the following statements is INCORRECT concerning the classical hypothesis testing framework?

- Key (A): If the null hypothesis is rejected, the alternative is accepted
- Models (C): The test of significance and confidence interval approaches will always give the same conclusions
- Note: Rejecting the null does not mean the alternative is accepted; the key is the incorrect statement. Reviewer: Claude, needs human confirmation.

## mmlupro-10893 (philosophy): **key_wrong**

According to Stevenson, moral disagreements involve:

- Key (E): disagreement in interest.
- Models (G): disagreement in attitude.
- Note: Stevenson: moral disagreement is disagreement in attitude (not interest). Reviewer: Claude, needs human confirmation.

## mmlupro-11051 (philosophy): **key_wrong**

Lukianoff and Haidt argue that American colleges and universities now encourage

- Key (B): critical reasoning.
- Models (A): emotional reasoning.
- Note: Lukianoff and Haidt argue colleges encourage emotional reasoning, which undermines critical thinking. Reviewer: Claude, needs human confirmation.

## mmlupro-3341 (biology): **key_wrong**

If a ring is cut through the bark all the way around a tree, down to the wood, the tree will live for a while, then die. Explain why.

- Key (G): The tree will eventually die because the cut severs the vascular system, preventing water and nutrients from being transported from the roots to the upper part of the tree and vice versa. This leads to a gradual loss of turgidity, closure of stomata, suspension of photosynthesis, and exhaustion of food reserves.
- Models (F): The tree will die because the cut disrupts the flow of energy from the leaves to the roots, leading to the roots' starvation.
- Note: Girdling removes the phloem (in the bark); the xylem (wood) is intact, so water still moves up. The tree dies because the roots starve, which is F. G's claim that water from the roots is blocked is wrong. Reviewer: Claude.

## mmlupro-3576 (chemistry): **key_wrong**

When a swimmer leaves cold water on a warm, breezy day, he experiences a cooling effect. Why?

- Key (F): The water removes heat from the swimmer's body.
- Models (C): Evaporation of water from the swimmer's skin cools the body down.
- Note: Cooling after leaving water is due to evaporation from the skin (C). Reviewer: Claude, needs human confirmation.

## mmlupro-3646 (chemistry): **key_wrong**

Another application of the relationship given in Problem $1-48$ has to do with the excitedstate energies and lifetimes of atoms and molecules. If we know that the lifetime of an excited state is $10^{-9} \mathrm{~s}$, then what is the uncertainty in the energy of this state?

- Key (C): 7 $10^{-25} \mathrm{~J}$
- Models (J): 1 $10^{-25} \mathrm{~J}$
- Note: Delta E ~ hbar/delta t = 1.05e-25 J, matching J, not 7e-25 J. Reviewer: Claude, needs human confirmation.

## mmlupro-4173 (chemistry): **key_wrong**

The duration of a $90^{\circ}$ or $180^{\circ}$ pulse depends on the strength of the $\mathscr{B}_1$ field. If a $180^{\circ}$ pulse requires $12.5 \mu \mathrm{s}$, what is the strength of the $\mathscr{B}_1$ field?

- Key (H): 5.9 $10^{-4} \mathrm{~T}$
- Models (G): 9.3 $10^{-4} \mathrm{~T}$
- Note: B1 = pi/(gamma*t) with proton gamma 2.675e8 and t=12.5 us gives 9.4e-4 T, matching G. Reviewer: Claude, needs human confirmation.

## mmlupro-4219 (chemistry): **key_wrong**

The unaided eye can perceive objects which have a diameterof 0.1 mm. What is the diameter in inches?

- Key (D): 3.94 ×10^3 inches
- Models (H): 0.003937 inches
- Note: 0.1 mm = 0.003937 in; the key 3.94e3 inches is off by a factor of 1e6. Reviewer: Claude, needs human confirmation.

## mmlupro-4683 (history): **key_wrong**

This question refers to the following information.
"We found that not only was it a civil war, an effort by a people who had for years been seeking their liberation from any colonial influence whatsoever, but also we found that the Vietnamese whom we had enthusiastically molded after our own image were hard put to take up the fight against the threat we were supposedly saving them from.
"We found most people didn't even know the difference between communism and democracy. They only wanted to work in rice paddies without helicopters strafing them and bombs with napalm burning their villages and tearing their country apart. They wanted everything to do with the war, particularly with this foreign presence of the United States of America, to leave them alone in peace, and they practiced the art of survival by siding with whichever military force was present at a particular time, be it Viet Cong, North Vietnamese or American."
John Kerry, 1971
Which of the following pairs of words best characterizes the differences between the approaches of Presidents Lyndon Johnson (1963–1969) and Richard Nixon (1969–1974) to the Vietnam conflict?

- Key (D): Insurgence vs. retreat
- Models (F): Escalation vs. de-escalation
- Note: Johnson escalated, Nixon de-escalated (Vietnamization): 'escalation vs de-escalation'. Reviewer: Claude, needs human confirmation.

## mmlupro-4701 (history): **key_wrong**

Unlike most other early civilizations, Minoan culture shows little evidence of:

- Key (D): conspicuous consumption by elites.
- Models (B): warfare.
- Note: Minoan culture is distinctive for showing little evidence of warfare. Reviewer: Claude, needs human confirmation.

## mmlupro-4987 (history): **key_wrong**

This question refers to the following information.
"The Italian nation has been at last united in our own days, and we all rejoiced in its union. Yet we may be allowed to doubt whether the union was not a little too speedy and a little too thorough. It is surely carrying unity too far to wipe out all traces of the independent being, for most purposes to wipe out the very name, of such a land as Sicily. It jars on our feelings to find that, while Ireland at least forms part of the royal style of its sovereign, Sicily is no longer even a geographical expression. The island realm of Roger has sunk to be seven provinces of the kingdom on the mainland. And there is another result of Italian unity, a result in which we may rejoice without drawbacks, but which still has somewhat of sadness about it as finally ending that great phase of the history of Europe with which we have throughout been dealing. Never were ties with the past so fully snapped as when the army of Italy entered liberated Rome. Of all novelties in European history the greatest was when Rome became the centre of a dominion with acknowledged metes and bounds, the head in short of a local Italian kingdom. "Rome the capital of Italy" was a formula which might well gladden our hearts; but it was a formula which formally swept away the œcumenical position, the œcumenical traditions, of Rome&….
But the kingdom of Italy is not an appendage to Rome; Rome is the head of the kingdom. The whole is greater than its part; Rome, by her own free will and by the free will of Italy, has become less than Italy. By becoming the willing head of an Italian kingdom she has formally cast aside her Imperial traditions as they were not cast aside when brute force made her the head of a French department."
Edward A. Freeman, British historian and politician, The Chief Periods of European History, 1885
According to the author, Italy's connections to its history and traditions were most "fully snapped" when

- Key (B): French troops abandoned Rome to fight in the Franco-Prussian War.
- Models (E): Italy's army entered Rome.
- Note: The passage says ties were fully snapped when the army of Italy entered Rome. Reviewer: Claude, needs human confirmation.

## mmlupro-5863 (other): **key_wrong**

In which year was the seminal Human Development Report published?

- Key (D): 1994
- Models (H): 1990
- Note: The first Human Development Report was published by UNDP in 1990 (H), not 1994. Reviewer: Claude.

## mmlupro-6214 (health): **key_wrong**

Which of the following is NOT one of the more frequently named activities by those who are retired?

- Key (G): Redoing the home
- Models (H): DJing at local clubs
- Note: Redoing the home is a common retiree activity; DJing at clubs is the NOT-one. Reviewer: Claude, needs human confirmation.

## mmlupro-6224 (health): **key_wrong**

In which of the following positions does a patient lie face down?

- Key (B): Erect
- Models (D): Prone
- Note: Prone means lying face down; erect is upright. Reviewer: Claude, needs human confirmation.

## mmlupro-684 (business): **key_wrong**

In the _________ stage in the adoption process, consumers become aware of the new proposition. They have little information and have yet to develop any particular attitudes towards the product. Indeed, at this stage consumers are not interested in finding out any more information.

- Key (D): Knowledge
- Models (B): Awareness
- Note: The stem describes the awareness stage. Reviewer: Claude, needs human confirmation.

## mmlupro-6931 (economics): **key_wrong**

Define Gross National Product (GNP).

- Key (C): The total market value of all final goods and services produced in the economy in one year
- Models (J): The total value of all goods and services produced by a nation's residents, regardless of the location
- Note: GNP counts output of a nation's residents wherever located; the key describes GDP. Reviewer: Claude, needs human confirmation.

## mmlupro-9384 (physics): **key_wrong**

What is the impedance of a 1-henry inductor at angular frequencies of 100, 1000 and 10,000rad/sec?

- Key (H): 1000 ohms, 10000 ohms, 100 ohms
- Models (B): 100 ohms, 1000 ohms, 10,000 ohms
- Note: X_L = wL with L = 1 H gives 100, 1000, 10000 ohms in the order asked (B). H lists the same values in a scrambled order. Reviewer: Claude.

## mmlupro-9682 (physics): **key_wrong**

The first five harmonics produced by an organ pipe open at both ends are 50 Hz, 100 Hz, 150 Hz, 200 Hz, and 250 Hz. Which of the harmonics, if any, will survive once the pipe is closed at one end?

- Key (E): nan
- Models (H): No harmonics will survive
- Note: The key option's text is missing ('nan'); odd harmonics 50, 150, 250 Hz survive. Reviewer: Claude, needs human confirmation.

## mmlupro-10495 (computer science): **unreviewed**

What does EXE do when the STP solver times out on a constraint query for a particular path?

- Key (A): Assume that the query is not satisfiable and stop executing the path
- Models (E): Assume that the query is satisfiable and continue executing the path.

## mmlupro-10704 (computer science): **unreviewed**

Write a skeletal format of C programs.

- Key (D): [constant declarations] [externals] main ( ) { [program statements] } [additional functions]
- Models (B): [function prototypes] [globals] main ( ) { [control structures] } [subroutines]

## mmlupro-11195 (philosophy): **unreviewed**

Ashford argues that worries about causing dependency on aid agencies among those in extreme poverty does not mean that we should

- Key (I): adopt a social contract approach to the problem of global economic justice.
- Models (B): abandon the world's poor to their unjust predicament.

## mmlupro-11269 (philosophy): **unreviewed**

According to Lukianoff and Haidt, institutionalizing vindictive protectiveness will

- Key (C): harm their ability to learn.
- Models (D): all of the above.

## mmlupro-11271 (philosophy): **unreviewed**

Papadaki thinks that in cases where partners in a relationship mutually deny each other's humanity that

- Key (G): there is no straightforward answer to the question of whether or not sexual objectification occurs.
- Models (B): sexual objectification occurs.
- Note: Needs someone who knows Papadaki's paper on sexual objectification. Kept until reviewed.

## mmlupro-11883 (engineering): **unreviewed**

Consider a thoroughly mixed vessel where a salt is dis-solved inwater. The volume of the fresh water initially in the tank is 100lbm.The inlet conditions are,ṁ_w= 150 lb/hr. and ṁ_s= 30 lb/hr. The resulting solution leaves at a rate of 120 lb/hr. If the flow in and out remain constant, compute the outletconcentration after one hour.

- Key (F): 0.26
- Models (D): 0.16

## mmlupro-12061 (engineering): **unreviewed**

Calculate the minimum power required to cool 100 lb moles / min of air from 550°R to 500°R when the surrounding temperature is 550°R.

- Key (A): - 1600 Btu/min or - 37.7 hp
- Models (J): - 1700 Btu/min or - 40.7 hp

## mmlupro-1644 (law): **unreviewed**

A man committed a series of heinous crimes, including a kidnapping, that took him across state lines and violated federal law. He was convicted and received a life sentence. The felon, however, was pardoned by the President of the United States, who was a childhood friend. A great hue and cry ensued, and the talking heads on television proclaimed that legislation was needed to prevent such injustice again. Would such legislation be constitutional?

- Key (I): No. While what the president did wasn't a good idea, the Constitution expressly grants the President an unqualified power to pardon.
- Models (A): No, because the president's power to pardon can only be limited by a constitutional amendment.

## mmlupro-1908 (law): **unreviewed**

A pedestrian was injured when hit by a chair that was thrown from an upper-story hotel window. The pedestrian sued the occupants of all the rooms from which the chair might have been thrown. At trial, the pedestrian has been unable to offer any evidence as to the exact room from which the chair was thrown. The defendants have filed a motion for a directed verdict. Should the court grant the motion?

- Key (A): Yes, because the pedestrian has failed to offer evidence that the defendants jointly engaged in tortious conduct.
- Models (F): No, because of the doctrine of alternative liability.

## mmlupro-2017 (psychology): **unreviewed**

Learned helplessness is an example of the power of

- Key (G): expectation
- Models (H): operant conditioning

## mmlupro-2080 (psychology): **unreviewed**

Dr. Marcos Manzetti uses a “sliding scale” that is based on a client’s current income to set his fees for therapy. Dr. Manzetti’s practice is:

- Key (D): ethically acceptable since it serves the best interests of his clients.
- Models (B): ethically acceptable, as it provides opportunities for those with lower income.

## mmlupro-2432 (psychology): **unreviewed**

On average, men perform better than women on all the following tasks with the exception of:

- Key (E): Simultaneous processing
- Models (D): Emotional intelligence tests

## mmlupro-2749 (psychology): **unreviewed**

What does research suggest is the major result of breastfeeding an infant?

- Key (C): the attitude the parents have towards the child during feeding time
- Models (I): intimate contact with the mother

## mmlupro-3440 (biology): **unreviewed**

A researcher grows a population of ferns in her laboratory. She notices, after a few generations, a new variant that has a distinct phenotype. When she tries to breed the original phenotype with the new one, no offspring are produced. When she breeds the new variants, however, offspring that look like the new variant result. Which of the following is likely to exhibit the process described earlier?

- Key (D): Grass
- Models (F): Wheat

## mmlupro-4424 (chemistry): **unreviewed**

Which of the following is expected to be the least soluble in water?

- Key (C): NiSO3
- Models (A): Cu(OH)2

## mmlupro-4910 (history): **unreviewed**

Which continent features the earliest evidence of etching into a rock face?

- Key (I): Australia
- Models (B): Africa

## mmlupro-5025 (history): **unreviewed**

This question refers to the following information.
Read the following quote.
I had now decided beyond all question that there existed in the heavens three stars wandering about Jupiter as do Venus and Mercury about the sun, and this became plainer than daylight from observations on similar occasions which followed. Nor were there just three such stars; four wanderers complete their revolutions about Jupiter, and of their alterations as observed more precisely later on we shall give a description here. Also I measured the distances between them by means of the telescope. . . .
Such are the observations concerning the four Medicean planets recently first discovered by me, and although from this data their periods have not yet been reconstructed in numerical form, it is legitimate at least to put in evidence some facts worthy of note. Above all, since they sometimes follow and sometimes precede Jupiter by the same intervals, and they remain within very limited distances either to east or west of Jupiter, accompanying that planet in both its retrograde and direct movements in a constant manner, no one can doubt that they complete their revolutions about Jupiter and at the same time effect all together a twelve-year period about the center of the universe.
—Galileo Galilei, 1610
Which of the following intellectual hallmarks of the Renaissance seem most in conflict with the questioning of the ancient philosophers, such as Aristotle, through experimentation in natural philosophy?

- Key (A): Humanism
- Models (I): Classicism

## mmlupro-5135 (other): **unreviewed**

Which of the following is NOT a good predictor of which states will get nuclear weapons?

- Key (C): Regime type
- Models (B): Age of the state

## mmlupro-5284 (other): **unreviewed**

Which of these qualities is NOT listed as something to consider when choosing an opinion leader for a public relations campaigns?

- Key (C): Familiarity with subject or issue
- Models (B): Impact

## mmlupro-5290 (other): **unreviewed**

In what ways may TNC be regarded as a new concept?

- Key (B): Transnational organized criminal activities consist of profit driven crime for a high level return that may result in the subversion or infiltration of the legal economy through the reinvestment of illicit profits.
- Models (D): The terms 'transnational crime' and 'organized crime' are sometimes used interchangeably but not all transnational crime will be committed by an organized group nor will all organized groups engage in transnational crime. The pursuit of profit for illicit activity eludes definition and may include those individuals or businesses that engage in occasional transnational criminal activity but are otherwise legitimate operatives.

## mmlupro-6519 (health): **unreviewed**

The replication of hepatitis B includes which of the following stages?

- Key (C): Virions produced in the cytoplasm by cellular DNA polymerase
- Models (B): Conversion of relaxed circular viral DNA in to covalently closed circular (CCC) DNA in the nucleus

## mmlupro-9599 (physics): **unreviewed**

Show how two clocks, one at the origin and the other a dis-tance d from the origin, may be synchronized.

- Key (D): The other clock should be pre-set so that it reads 12:00 o'clock plus d/c
- Models (E): The other clock should be pre-set so that it reads d/c past the time on the origin clock
