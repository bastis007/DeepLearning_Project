"""
In this file, we want to read the predictions from the predictions file of the model
and use the metrics to evaluate the quality.
"""
from torchmetrics.text import TranslationEditRate
from torchmetrics.text.bert import BERTScore
from torchmetrics.text.bleu import BLEUScore
from torchmetrics.text.rouge import ROUGEScore
from torchmetrics.text.wer import WordErrorRate

# Define the Name of the models
method_name = ['CNN_Basic', 'CNN_Auto_Bigger', 'CNN_Auto_Basic']


def use_metrics(predicted_text, ground_truth_text):
    results = []
    # BLEU
    bleu = BLEUScore()
    bleu_score = bleu(predicted_text, ground_truth_text)
    results.append("BLEU: " + str(bleu_score.item()))
    # TER
    ter = TranslationEditRate()
    ter_score = ter(predicted_text, ground_truth_text)
    results.append("TER: " + str(ter_score.item()))
    # ROUGE
    rouge = ROUGEScore()
    rouge_score = rouge(predicted_text, ground_truth_text)
    results.append("ROUGE1 Fmeasure: " + str(rouge_score['rouge1_fmeasure'].item()))
    results.append("ROUGE1 Precision: " + str(rouge_score['rouge1_precision'].item()))
    results.append("ROUGE2 Fmeasure: " + str(rouge_score['rouge2_fmeasure'].item()))
    results.append("ROUGE2 Precision: " + str(rouge_score['rouge2_precision'].item()))
    # WER
    wer = WordErrorRate()
    wer_score = wer(predicted_text, ground_truth_text)
    results.append("WER: " + str(wer_score.item()))
    # BERT
    #bert = BERTScore()
    #if not predicted_text:
        #bert_score = "None"
    #else:
        #bert_score = bert(predicted_text, ground_truth_text)
    #results.append("BERT: " + str(bert_score))
    #return results


def write_metric_results(results, method):
    print(method)
    with open(f'./evaluation/eval_metrics_{method}.txt', 'a', encoding='utf-8') as file:
        file.write("Evaluation Metrics for " + str(method) + "\n" + str(results))


for i in range(len(method_name)):
    with open(f'./predictions/model_predictions_{method_name[i]}.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            if "Predicted (French): " in line:
                prediction = line.split("Predicted (French): ")[1]
            elif "Ground Truth (French): " in line:
                ground_truth = line.split("Ground Truth (French): ")[1]
            elif "----------" in line:
                metric_results = use_metrics(prediction, ground_truth)
                print(metric_results)
                write_metric_results(metric_results, method_name[i])
                print("Results written")
