%question1
%Codon table
codon(ttt,f).
codon(tct,s).
codon(tat,y).
codon(tgt,c).
codon(ttc,f).
codon(tcc,s).
codon(tac,y).
codon(tgc,c).
codon(tta,l).
codon(tca,s).
codon(taa,stop).
codon(tga,stop).
codon(ttg,l).
codon(tcg,s).
codon(tag,stop).
codon(tgg,w).
codon(ctt,l).
codon(cct,p).
codon(cat,h).
codon(cgt,r).
codon(ctc,l).
codon(ccc,p).
codon(cac,h).
codon(cgc,r).
codon(cta,l).
codon(cca,p).
codon(caa,q).
codon(cga,r).
codon(ctg,l).
codon(ccg,p).
codon(cag,q).
codon(cgg,r).
codon(att,i).
codon(act,t).
codon(aat,n).
codon(agt,s).
codon(atc,i).
codon(acc,t).
codon(aac,n).
codon(agc,s).
codon(ata,i).
codon(aca,t).
codon(aaa,k).
codon(aga,r).
codon(atg,m).
codon(acg,t).
codon(aag,k).
codon(agg,r).
codon(gtt,v).
codon(gct,a).
codon(gat,d).
codon(ggt,g).
codon(gtc,v).
codon(gcc,a).
codon(gac,d).
codon(ggc,g).
codon(gta,v).
codon(gca,a).
codon(gaa,e).
codon(gga,g).
codon(gtg,v).
codon(gcg,a).
codon(gag,e).
codon(ggg,g).
% Translation predicate
translate([], []).
translate([H|T], [RH|RT]) :-
    codon(H, RH),

    % if translated result is not stop
    RH \= stop,

    % ercursively call method transalte to translate codon
    translate(T, RT).
translate([_|_], []).

?- translate([atg,ttt,tct,taa], X).
X = [m, f, s]

?- translate([tag,ttt,tct,taa], X).
X = []

?- translate([], X).
X = []


